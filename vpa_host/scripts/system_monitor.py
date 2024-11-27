#! /usr/bin/env python3

import rospy

class SystemMonitor:

    def __init__(self) -> None:
        # Init ROS Node
        rospy.init_node('system_monitor')


        # Publishers


        # Subscribers


        # Serverss


        # ServiceProxys


        rospy.loginfo('System Monitor is Online')


if __name__ == '__main__':
    try:
        N = SystemMonitor()
        rospy.spin() 
    except rospy.ROSInterruptException:
        pass
