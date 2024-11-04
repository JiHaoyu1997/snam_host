#! /usr/bin/env python3

import rospy

import cv2
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

from hsv import HSVSpace

center_line_hsv             = HSVSpace(h_u=105, h_l=65,  s_u=255, s_l=100, v_u=255, v_l=205) 
side_line_hsv               = HSVSpace(h_u=100, h_l=25,  s_u=60,  s_l=0,   v_u=255, v_l=200) 
buffer_line_hsv             = HSVSpace(h_u=160, h_l=115, s_u=180, s_l=60, v_u=230, v_l=180) 
inter_boundary_line_hsv     = HSVSpace(h_u=50,  h_l=20,  s_u=255, s_l=200, v_u=170, v_l=120) 

# 定义HSV范围（可以根据实际情况调整）
HSV_RANGES = {
    'yellow': center_line_hsv,
    # 'white': side_line_hsv,
    # 'pink':buffer_line_hsv,
    # 'green':inter_boundary_line_hsv
}

class ImageProcessor:

    def __init__(self) -> None:

        rospy.init_node('image_processor')

        self.bridge = CvBridge()

        self.cv_image_pub = rospy.Publisher("/image_processor/cv_image", Image, queue_size=1)

        self.result_cv_image_pub = rospy.Publisher("/image_processor/result_cv_image", Image, queue_size=1)

        self.mask_image_pub = rospy.Publisher("/image_processor/mask_image", Image, queue_size=1)

        self.overexposed_mask_image_pub = rospy.Publisher("/image_processor/overexposed_mask_image", Image, queue_size=1)

        self.image_raw_sub = rospy.Subscriber("/henry/robot_cam/image_raw", Image, self.image_raw_sub_cb)

        rospy.loginfo('Image Processor is Online')

    def image_raw_sub_cb(self, data: Image):
        start_time = time.time()
        try:
            cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        cv_img_raw = cv_img[int(cv_img.shape[0]/4) : cv_img.shape[0], :]

        cv_img_raw2 = self.adjust_gamma(cv_img=cv_img_raw, gamma=0.5)

        result_cv_img = self.recover_overexposed_area(cv_img_raw=cv_img_raw2)

        self.pub_cv_img(cv_img=cv_img_raw2)

        self.pub_result_cv_img(result_cv_img=result_cv_img)

        end_time = time.time()

        print(f"processing time is: {end_time - start_time:.4f} seconds")

        return     

    def recover_overexposed_area(self, cv_img_raw):
        height, width, _ = cv_img_raw.shape
        result_image = cv_img_raw.copy()
        cv_hsv_img = cv2.cvtColor(cv_img_raw, cv2.COLOR_RGB2HSV) 

        # 迭代每种颜色
        for hsv in HSV_RANGES.values():
            mask_img = hsv.apply_mask(hsv_image=cv_hsv_img)         
            overexposed_mask_img = cv2.inRange(cv_hsv_img, (0, 0, 225), (255, 50, 255))  # 亮度阈值，定义过曝

            color_contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            overexposed_contours, _ = cv2.findContours(overexposed_mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            self.pub_mask_img(mask_img=mask_img)
            self.pub_overexposed_mask_img(overexposed_mask_img=overexposed_mask_img)

            # print("Total contours found:", len(color_contours))
      
            # Process each overexposed contour
            for overexposed_contour in overexposed_contours:
                is_connected_to_color = False
                for color_contour in color_contours:
                    for point in overexposed_contour:
                        pt = (int(point[0][0]), int(point[0][1]))
                        if cv2.pointPolygonTest(color_contour, pt, False) >= 0:
                            is_connected_to_color = True
                            break
                    if is_connected_to_color:
                        break
           
                # Only restore areas connected to color contours
                if is_connected_to_color:
                    # Create a mask for the current overexposed contour
                    overexposed_area_mask = np.zeros((height, width), dtype=np.uint8)
                    cv2.drawContours(overexposed_area_mask, [overexposed_contour], -1, 255, thickness=cv2.FILLED)
                    
                    # Find non-overexposed neighbors in the color mask
                    for y, x in zip(*np.where(overexposed_area_mask > 0)):
                        replaced = False
                        for dy in range(-5, 6):
                            if replaced:
                                break
                            for dx in range(-5, 6):
                                ny, nx = y + dy, x + dx
                                if 0 <= ny < height and 0 <= nx < width and mask_img[ny, nx] > 0:
                                    result_image[y, x] = [255, 0, 0]
                                    replaced = True
                                    break

        return result_image
    
    def cv_show(self, name, img):
        # 检查图像是否为空
        if img is None:
            print(f"Error: Unable to display {name}, image not loaded.")
            return
        
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def pub_cv_img(self, cv_img):
        cv_img_copy = cv_img
        cv_img_copy_msg = self.bridge.cv2_to_imgmsg(cv_img_copy, encoding="bgr8")
        cv_img_copy_msg.header.stamp = rospy.Time.now()
        self.cv_image_pub.publish(cv_img_copy_msg)
        return   
    
    def pub_result_cv_img(self, result_cv_img):
        cv_img_copy = result_cv_img
        cv_img_copy_msg = self.bridge.cv2_to_imgmsg(cv_img_copy, encoding="bgr8")
        cv_img_copy_msg.header.stamp = rospy.Time.now()
        self.result_cv_image_pub.publish(cv_img_copy_msg)
        return 
        
    def pub_overexposed_mask_img(self, overexposed_mask_img):
        mask_img_msg = self.bridge.cv2_to_imgmsg(overexposed_mask_img, encoding="passthrough")
        mask_img_msg.header.stamp = rospy.Time.now()
        self.overexposed_mask_image_pub.publish(mask_img_msg)
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

if __name__ == '__main__':
    try:
        image_processor_node = ImageProcessor()
        rospy.spin()  # 保持节点运行，处理回调
    except rospy.ROSInterruptException:
        pass