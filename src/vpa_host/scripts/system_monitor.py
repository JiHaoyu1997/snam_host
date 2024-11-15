#! /usr/bin/env python3

import rospy

import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

import search_pattern
from hsv import HSVSpace
from map import map

# Msg
from sensor_msgs.msg import Image

from utils.utils import resize_images_to_same_height

class SystemMonitor:

    def __init__(self) -> None:
        # Init ROS Node
        rospy.init_node('system_monitor')

        self.bridge = CvBridge()

        #
        self.color_space_init()

        # Publishers
        self.cv_image_pub = rospy.Publisher("cv_image", Image, queue_size=1)
        self.mask_image_pub = rospy.Publisher("mask_image", Image, queue_size=1)

        # Subscribers
        self.image_raw_sub = rospy.Subscriber("/luna/robot_cam/image_raw", Image, self._image_raw_sub_cb)

        # Servers
        # (如果需要的话可以在这里定义服务)

        # ServiceProxy
        # (如果需要的话可以在这里定义服务代理)


        rospy.loginfo('System Monitor is Online')

    def color_space_init(self) -> None:
        # 
        self.center_x = rospy.get_param('~center_x', 160)
        self.center_y = rospy.get_param('~center_y', 90)

        # HSV space for Yellow (center lane line)
        self.center_line_hsv = HSVSpace(
            h_u=int(rospy.get_param('~h_upper_1', 105)),
            h_l=int(rospy.get_param('~h_lower_1', 65)),
            s_u=int(rospy.get_param('~s_upper_1', 255)),
            s_l=int(rospy.get_param('~s_lower_1', 100)),
            v_u=int(rospy.get_param('~v_upper_1', 255)),
            v_l=int(rospy.get_param('~v_lower_1', 205))
        ) 

        # HSV space for White (side lane line)
        self.side_line_hsv = HSVSpace(
            h_u=int(rospy.get_param('~h_upper_2', 100)),
            h_l=int(rospy.get_param('~h_lower_2', 25)),
            s_u=int(rospy.get_param('~s_upper_2', 60)),
            s_l=int(rospy.get_param('~s_lower_2', 0)),
            v_u=int(rospy.get_param('~v_upper_2', 255)),
            v_l=int(rospy.get_param('~v_lower_2', 200))
        ) 

        # HSV space for Red (stop line)
        self.stop_line_hsv = HSVSpace(
            h_u=int(rospy.get_param('~h_upper_s', 140)),
            h_l=int(rospy.get_param('~h_lower_s', 100)),
            s_u=int(rospy.get_param('~s_upper_s', 210)),
            s_l=int(rospy.get_param('~s_lower_s', 190)),
            v_u=int(rospy.get_param('~v_upper_s', 200)),            
            v_l=int(rospy.get_param('~v_lower_s', 160))
        )

        # Buffer Line HSV - Pink
        self.buffer_line_hsv = HSVSpace(160, 120, 180, 140, 220, 180)

        # Ready Line HSV - Yellow
        self.ready_line_hsv = HSVSpace(105, 65, 255, 205, 255, 205)

        # Intersection Boundary Line HSV - Green
        self.inter_boundary_line_hsv = HSVSpace( 50,  20, 255, 200, 170, 120)

        # guiding lines inside intersections - no dynamic reconfigure
        self._right_guide_hsv = HSVSpace(140, 100, 180, 140, 220, 180)
        self._left_guide_hsv  = HSVSpace(160, 125, 210, 170, 160, 135)
        self._thur_guide_hsv  = HSVSpace( 30,   0, 250, 200, 160, 110)  
        self.inter_guide_line = [self._thur_guide_hsv, self._left_guide_hsv, self._right_guide_hsv]

        # 
        self._acc_aux_hsv     = HSVSpace(150, 110, 180, 100, 255, 120)       


    def _image_raw_sub_cb(self, data: Image):
        # the function is supposed to be called at about 10Hz based on fps settins  
        try:
            cv_img_raw = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)        

        # the top 1/3 part of image_raw for acc function
        acc_img = cv_img_raw[0 : int(cv_img_raw.shape[0]/3), :]

        # the bottom 3/4 part of image_raw for tracking function
        cv_img_raw2 = cv_img_raw[int(cv_img_raw.shape[0]/4) : cv_img_raw.shape[0], :]

        # Image Operation
        cv_img = self.adjust_gamma(cv_img=cv_img_raw2, gamma=0.5)

        # convert BGR image to HSV image
        acc_hsv_img = self.from_cv_to_hsv(acc_img)
        cv_hsv_img = self.from_cv_to_hsv(cv_img)

        mask_img = self.center_line_hsv.apply_mask(cv_hsv_img)

        def _search_lane_linecenter(_mask,_upper_bias:int,_lower_bias:int,_height_center:int,_interval:int,_width_range_left:int,_width_range_right:int) -> int:
            for i in range(_lower_bias,_upper_bias,_interval):
                point = np.nonzero(_mask[_height_center+i,_width_range_left:_width_range_right])[0] + _width_range_left
                if len(point) > 8 and len(point) < 45:
                    _line_center = int(np.mean(point))
                    return _line_center
                else:
                    continue
            return 0 # nothing found in the end
        
        _line_center1 = _search_lane_linecenter(mask_img,50,-20,int(cv_hsv_img.shape[0]/2),10,0,int(cv_hsv_img.shape[1]))
        
        self.pub_mask_img(mask_img=mask_img)
        return


        self.curr_route = [6, 2, 5]
        target_x = self.get_target_to_cross_conflict(cv_hsv_img=cv_hsv_img, cv_img=cv_img)
        self.target_x = target_x            
        self.pub_cv_img(cv_img=cv_img)
        return

    def from_cv_to_hsv(self, in_image):
        return cv2.cvtColor(in_image, cv2.COLOR_bgr2hsv)
    
    def get_target_to_cross_conflict(self, cv_img, cv_hsv_img):
        self.next_action = map.local_mapper(last=self.curr_route[0], current=self.curr_route[1], next=self.curr_route[2])
        mask_img = self.inter_guide_line[self.next_action].apply_mask(cv_hsv_img)
        self.pub_mask_img(mask_img=mask_img[0:90, :])
        target_x = search_pattern.search_inter_guide_line2(self.inter_guide_line[self.next_action], cv_hsv_img, self.next_action)
        if target_x == None:
            target_x = 160
        cv2.circle(cv_img, (int(target_x), int(cv_hsv_img.shape[0]/2)), 5, (255, 255, 0), 5)
        return target_x
    
    def pub_cv_img(self, cv_img):
        cv_img_copy = cv_img
        cv_img_copy_msg = self.bridge.cv2_to_imgmsg(cv_img_copy, encoding="bgr8")
        cv_img_copy_msg.header.stamp = rospy.Time.now()
        self.cv_image_pub.publish(cv_img_copy_msg)
        return   
        
    def pub_mask_img(self, mask_img):
        mask_img_msg = self.bridge.cv2_to_imgmsg(mask_img, encoding="passthrough")
        mask_img_msg.header.stamp = rospy.Time.now()
        self.mask_image_pub.publish(mask_img_msg)
        return

    def adjust_gamma(self, cv_img, gamma=1.0):
        invGamma = 1.0 / gamma
        lookup_table = np.array([ (i /255.0) ** invGamma * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(cv_img, lookup_table)

    def cv_show(self, name, img):
        # 检查图像是否为空
        if img is None:
            print(f"Error: Unable to display {name}, image not loaded.")
            return
        
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        system_monitor_node = SystemMonitor()
        rospy.spin()  # 保持节点运行，处理回调
    except rospy.ROSInterruptException:
        pass
