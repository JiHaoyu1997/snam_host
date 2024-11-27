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

        self.pose_data_list = np.array((1, 6))

        self.first_flag = True

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
            for i in range(_num_of_detect):
                _data = _detections[i]
                id = _data.id[0]
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
                
                if self.first_flag:
                    self.pose_data_list = pose_data_np
                    self.first_flag = False
                else:
                    self.pose_data_list = np.vstack((self.pose_data_list, pose_data_np))
                
                # Print for easy visualization (optional, can be removed later)
                rospy.loginfo(f"Robot: {robot_dict[id]}, Time: {secs}.{nsecs}, Position: ({x}, {y}), Yaw: {yaw}")
                          
        return


if __name__ == '__main__':
    try:
        N = TimeTrajectoryMonitor()
        rospy.spin() 
    except rospy.ROSInterruptException:
        pass
