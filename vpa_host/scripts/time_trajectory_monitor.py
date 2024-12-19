#! /usr/bin/env python3

import rospy

import threading
import numpy as np
import matplotlib.pyplot as plt
from tf.transformations import euler_from_quaternion

from robot.robot import robot_dict

from apriltag_ros.msg import AprilTagDetectionArray
from vpa_robot_interface.msg import WheelsEncoder
from vpa_host.msg import KinematicData, KinematicDataArray

class TimeTrajectoryMonitor:
    def __init__(self) -> None:
        # Initialize the ROS node
        rospy.init_node('time_trajectory_monitor')

        # Data storage and thread management
        self.pose_data_dict = {}  # Historical data for each tag: {robot_id: [(timestamp, x, y, yaw)]}
        self.velocity_dict = {}  # Smoothed velocity for each tag: {robot_id: (linear_velocity, angular_velocity)}
        self.max_velocity_dict = {}
        self.zero_vel_counter = 0
        self.lock = threading.Lock()  # Thread lock for data synchronization

        # Publisher
        self.kinematic_info_pub = rospy.Publisher('/kinematic_info', KinematicDataArray, queue_size=10)

        # Subscriber
        self.pose_array_sub = rospy.Subscriber('/indoor_loc/tag_detections', AprilTagDetectionArray, self.pose_array_sub_cb)

        # Start a separate thread to calculate velocities
        self.compute_thread = threading.Thread(target=self.compute_velocity_loop)
        self.compute_thread.daemon = True
        self.compute_thread.start()

        rospy.loginfo('Time Trajectory Monitor is Online')

        self.timer = rospy.Timer(rospy.Duration(1 / 10), self.pub_kinematic_data)


    def pose_array_sub_cb(self, msg: AprilTagDetectionArray):
        """
        Callback function for the AprilTag detection topic.
        Extracts information for all detected tags and stores it.
        """
        if len(msg.detections) == 0:
            return  # Skip if no tags are detected

        # Extract timestamp
        secs = msg.header.stamp.secs
        nsecs = msg.header.stamp.nsecs
        timestamp = secs + nsecs / 1e9  # Convert to seconds

        # Iterate through all detected tags and update their data
        with self.lock:
            for detection in msg.detections:
                tag_id = detection.id[0]
                robot_id = tag_id
                
                if robot_id == 0:
                    continue

                x = detection.pose.pose.pose.position.x
                y = detection.pose.pose.pose.position.y

                # Extract yaw from orientation quaternion
                _qx = detection.pose.pose.pose.orientation.x
                _qy = detection.pose.pose.pose.orientation.y
                _qz = detection.pose.pose.pose.orientation.z
                _qw = detection.pose.pose.pose.orientation.w
                _, _, yaw = euler_from_quaternion([_qx, _qy, _qz, _qw])

                # Initialize or update tag data
                if robot_id not in self.pose_data_dict:
                    self.pose_data_dict[robot_id] = []
                    self.velocity_dict[robot_id] = (0.0, 0.0)  # Linear and angular velocities

                
                # Round x, y, and yaw to 3 decimal places
                x, y, yaw = round(x, 3), round(y, 3), round(yaw, 3)

                self.pose_data_dict[robot_id].append((timestamp, x, y, yaw))
                if len(self.pose_data_dict[robot_id]) > 10:  # Limit buffer length to 10
                    self.pose_data_dict[robot_id].pop(0)
        
    def compute_velocity_loop(self):
        """
        Continuously computes velocities for all tracked tags in a separate thread.
        """
        ewma_alpha = 1  # EWMA smoothing factor
        rate = rospy.Rate(10)
        reset_threshold = 3 / rate.sleep_dur.to_sec()
        
        while not rospy.is_shutdown():
            with self.lock:
                for robot_id, pose_data in self.pose_data_dict.items():
                    # Skip computation if less than 10 data points
                    if len(pose_data) < 10:
                        continue 

                    # Initialize cumulative displacement and time
                    initial_time, initial_x, initial_y, initial_yaw = pose_data[0]
                    end_yaw = pose_data[-1][3]
                    total_displacement_x = 0.0
                    total_displacement_y = 0.0
                    total_time = pose_data[-1][0] - pose_data[0][0]

                    # Iterate through consecutive pose data and calculate displacement between consecutive points
                    for i in range(1, len(pose_data)):
                        curr_time, curr_x, curr_y, curr_yaw = pose_data[i]

                        # Calculate time difference
                        delta_time = curr_time - initial_time
                        if delta_time <= 0:
                            continue  # Skip if no valid time difference

                        # Calculate displacement (change between consecutive positions)
                        delta_x = curr_x - pose_data[i - 1][1]  # Difference between current x and previous x
                        delta_y = curr_y - pose_data[i - 1][2]  # Difference between current y and previous y

                        # Accumulate displacement and time
                        total_displacement_x += delta_x
                        total_displacement_y += delta_y
                        initial_time = curr_time  # Update reference time for next calculation

                    if total_time > 0:
                        # Calculate linear velocity using the total displacement and total time
                        linear_velocity = np.sqrt(total_displacement_x ** 2 + total_displacement_y ** 2) / total_time

                        # Calculate angular velocity (yaw change)
                        yaw_difference = end_yaw - initial_yaw
                        yaw_difference = (yaw_difference + np.pi) % (2 * np.pi) - np.pi  # Normalize yaw
                        angular_velocity = yaw_difference / total_time

                        # Apply EWMA for smoothing
                        smoothed_linear_velocity = ewma_alpha * linear_velocity + (1 - ewma_alpha) * self.velocity_dict[robot_id][0]
                        smoothed_angular_velocity = ewma_alpha * angular_velocity + (1 - ewma_alpha) * self.velocity_dict[robot_id][1]

                        if abs(smoothed_linear_velocity) < 0.05:
                            smoothed_linear_velocity = 0

                        if abs(smoothed_angular_velocity) < 0.05:
                            smoothed_angular_velocity = 0

                        # Update velocity dictionary
                        self.velocity_dict[robot_id] = (smoothed_linear_velocity, smoothed_angular_velocity)

                        # Update max vel record
                        if robot_id not in self.max_velocity_dict:
                            self.max_velocity_dict[robot_id] = (0.0, 0.0)

                        max_linear_velocity, max_angular_velocity = self.max_velocity_dict[robot_id]
                        self.max_velocity_dict[robot_id] = (
                            max(smoothed_linear_velocity, max_linear_velocity),
                            max(abs(smoothed_angular_velocity), max_angular_velocity),
                        )

                        if smoothed_linear_velocity == 0:
                            self.zero_vel_counter += 1
                        else:
                            self.zero_vel_counter = 0
                        
                        if self.zero_vel_counter >= reset_threshold:
                            self.max_velocity_dict[robot_id] = (0.0, 0.0)

                        # # Log the computation results
                        # if robot_id != 0:
                        #     rospy.loginfo(f"{robot_dict[robot_id]} - Linear Velocity: {smoothed_linear_velocity:.3f} m/s, Angular Velocity: {smoothed_angular_velocity:.3f} rad/s")
                        #     rospy.loginfo(f"{robot_dict[robot_id]} - Max Linear Velocity: {self.max_velocity_dict[robot_id][0]:.3f} m/s, Max Angular Velocity: {self.max_velocity_dict[robot_id][1]:.3f} rad/s")

            rate.sleep()


    def pub_kinematic_data(self, event):
        kinematic_data_msg = KinematicDataArray()

        for robot_id, pose_data_list in self.pose_data_dict.items():
            if not pose_data_list:
                continue

            if not self.velocity_dict[robot_id]:
                continue        

            pose_data_array = np.array(pose_data_list)   

            timestamp, x, y, yaw = pose_data_list[-1]
            # timestamp = pose_data_array[-1, 0] 
            # avg_x   = np.round(np.mean(pose_data_array[:, 1]), 3)
            # avg_y   = np.round(np.mean(pose_data_array[:, 2]), 3)
            # avg_yaw = np.round(np.mean(pose_data_array[:, 3]), 3)
            linear_velocity, angular_velocity = self.velocity_dict[robot_id]

            kinematic_data = KinematicData()
            kinematic_data.robot_id = robot_id
            kinematic_data.pose     = (timestamp, x, y, yaw)
            # kinematic_data.pose     = (timestamp, avg_x, avg_y, avg_yaw)
            kinematic_data.vel      = (linear_velocity, angular_velocity)

            # 将 KinematicData 添加到 KinematicDataArray 中
            kinematic_data_msg.data.append(kinematic_data)

        # 发布数据
        self.kinematic_info_pub.publish(kinematic_data_msg)


if __name__ == '__main__':
    try:
        monitor = TimeTrajectoryMonitor()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
