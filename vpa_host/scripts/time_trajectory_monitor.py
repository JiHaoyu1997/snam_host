#! /usr/bin/env python3

import rospy

import numpy as np

from tf.transformations import euler_from_quaternion
from robot.robot import robot_dict

from apriltag_ros.msg import AprilTagDetectionArray, AprilTagDetection

class TimeTrajectoryMonitor:

    def __init__(self) -> None:
        # Init ROS Node
        rospy.init_node('time_trajectory_monitor')

        self.previous_pose_data_dict = {}

        self.pose_data_list = np.empty((0, 6))

        # Publishers


        # Subscribers
        self.pose_array_sub = rospy.Subscriber('/indoor_loc/tag_detections', AprilTagDetectionArray, self.pose_array_sub_cb)


        # Servers


        # ServiceProxy


        rospy.loginfo('System Monitor is Online')


    def pose_array_sub_cb(self, msg: AprilTagDetectionArray):        
        secs = msg.header.stamp.secs
        nsecs = msg.header.stamp.nsecs

        _detections = AprilTagDetection()
        _detections = msg.detections
        _num_of_detect = len(_detections)

        if _num_of_detect > 0:
            self.pose_data_list = np.empty((0, 6))
            for i in range(_num_of_detect):                               
                _data = _detections[i]
                id = _data.id[0]
                if id == 0:
                    continue
                x = _data.pose.pose.pose.position.x
                y = _data.pose.pose.pose.position.y

                _temp_x = _data.pose.pose.pose.orientation.x
                _temp_y = _data.pose.pose.pose.orientation.y
                _temp_z = _data.pose.pose.pose.orientation.z
                _temp_w = _data.pose.pose.pose.orientation.w

                (roll, pitch, yaw) = euler_from_quaternion([_temp_x, _temp_y, _temp_z, _temp_w])

                # Round x, y, and yaw to 3 decimal places
                x = round(x, 3)
                y = round(y, 3)
                yaw = round(yaw, 3)

                pose_data = [secs, nsecs, id, x, y, yaw]
                pose_data_np = np.array(pose_data)
                
                self.pose_data_list = np.vstack((self.pose_data_list, pose_data_np))
                
                # Print for easy visualization (optional, can be removed later)
                rospy.loginfo(f"{robot_dict[id]} --- Time: {secs}.{nsecs}, Position: ({x}, {y}), Yaw: {yaw}")

    
                if id in self.previous_pose_data_dict:
                    # Call the function to calculate velocity and direction
                    self.calculate_velocity_and_direction(self.previous_pose_data_dict[id], pose_data_np, id)

                self.previous_pose_data_dict[id] = pose_data_np
                          
        return

    def calculate_velocity_and_direction(self, prev_pose, curr_pose, robot_id):
        """
        Calculate the robot's velocity and angular velocity.
        :param prev_pose: The pose data at the previous time step
        :param curr_pose: The pose data at the current time step
        :param robot_id: The ID of the robot
        """

        # Extract previous and current position and yaw
        prev_x, prev_y, prev_yaw = prev_pose[3], prev_pose[4], prev_pose[5]
        curr_x, curr_y, curr_yaw = curr_pose[3], curr_pose[4], curr_pose[5]
        print(prev_x, curr_x)

        # Calculate velocity (Euclidean distance between two points divided by time difference)
        dt = (curr_pose[0] + curr_pose[1] / 1e9) - (prev_pose[0] + prev_pose[1] / 1e9)  # Time difference in seconds
        distance = np.sqrt((curr_x - prev_x) ** 2 + (curr_y - prev_y) ** 2)  # Euclidean distance
        velocity = distance / dt if dt > 0 else 0  # Velocity in m/s

        # Calculate direction (change in yaw)
        yaw_diff = curr_yaw - prev_yaw
        if yaw_diff > np.pi:
            yaw_diff -= 2 * np.pi
        elif yaw_diff < -np.pi:
            yaw_diff += 2 * np.pi
        angular_velocity = yaw_diff / dt if dt > 0 else 0  # Angular velocity in rad/s

        # Print the velocity and angular velocity (direction change rate)
        rospy.loginfo(f"{robot_dict[robot_id]} --- Velocity: {velocity:.3f} m/s, Angular Velocity: {angular_velocity:.3f} rad/s")

        return


if __name__ == '__main__':
    try:
        N = TimeTrajectoryMonitor()
        rospy.spin() 
    except rospy.ROSInterruptException:
        pass
