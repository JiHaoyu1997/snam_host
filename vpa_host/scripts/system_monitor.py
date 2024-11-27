#! /usr/bin/env python3

import rospy

import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

import vpa_host.scripts.robot.search_pattern as search_pattern
from vpa_host.scripts.robot.hsv import HSVSpace
from map import map

# Msg
from sensor_msgs.msg import Image

class SystemMonitor:

    def __init__(self) -> None:
        # Init ROS Node
        rospy.init_node('system_monitor')

        self.bridge = CvBridge()

        #


        # Publishers


        # Subscribers


        # Servers


        # ServiceProxy


        rospy.loginfo('System Monitor is Online')


if __name__ == '__main__':
    try:
        N = SystemMonitor()
        rospy.spin() 
    except rospy.ROSInterruptException:
        pass
