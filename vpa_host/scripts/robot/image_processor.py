#! /usr/bin/env python3

import rospy

import cv2
import time
import numpy as np
from cv_bridge import CvBridge, CvBridgeError

from sensor_msgs.msg import Image

from vpa_host.scripts.robot.hsv import HSVSpace

HSV_RANGES = {
    'pink': HSVSpace(h_u=180, h_l=140, s_u=255, s_l=100, v_u=255, v_l=150),
    'yellow': HSVSpace(h_u=30, h_l=20, s_u=255, s_l=100, v_u=255, v_l=150),
    'red': HSVSpace(h_u=10, h_l=0, s_u=255, s_l=100, v_u=255, v_l=150),  # 或者 h_u=180, h_l=170
    'green': HSVSpace(h_u=80, h_l=50, s_u=255, s_l=100, v_u=255, v_l=50),
    'blue': HSVSpace(h_u=140, h_l=100, s_u=255, s_l=100, v_u=255, v_l=50),
    'white': HSVSpace(h_u=180, h_l=0, s_u=80, s_l=0, v_u=255, v_l=180),
    'purple': HSVSpace(h_u=160, h_l=130, s_u=255, s_l=100, v_u=255, v_l=50),
    'orange': HSVSpace(h_u=25, h_l=10, s_u=255, s_l=100, v_u=255, v_l=150)
}

class ImageProcessor:
    def __init__(self) -> None:
        rospy.init_node('image_processor')
        self.bridge = CvBridge()
        self.cv_image_pub = rospy.Publisher("/image_processor/cv_image", Image, queue_size=1)
        self.result_cv_image_pub = rospy.Publisher("/image_processor/result_cv_image", Image, queue_size=1)
        self.mask_image_pub = rospy.Publisher("/image_processor/mask_image", Image, queue_size=1)
        self.overexposed_mask_image_pub = rospy.Publisher("/image_processor/overexposed_mask_image", Image, queue_size=1)
        self.image_raw_sub = rospy.Subscriber("/lucas/robot_cam/image_raw", Image, self.image_raw_sub_cb)
        rospy.loginfo('Image Processor is Online')

    def image_raw_sub_cb(self, data: Image):
        start_time = time.time()
        try:
            cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
            cv_img_raw = cv_img[int(cv_img.shape[0] / 4):, :]  # Crop the image
            cv_img_raw2 = self.adjust_gamma(cv_img=cv_img_raw, gamma=0.5)
            # result_cv_img = self.recover_overexposed_area(cv_img_raw=cv_img_raw2)

            self.pub_cv_img(cv_img=cv_img_raw2)
            # self.pub_result_cv_img(result_cv_img=result_cv_img)
        except CvBridgeError as e:
            rospy.logerr(f"CV Bridge Error: {e}")
        except Exception as e:
            rospy.logerr(f"Unexpected error: {e}")

        end_time = time.time()
        rospy.loginfo(f"Processing time: {end_time - start_time:.4f} seconds")

    def recover_overexposed_area(self, cv_img_raw):
        height, width, _ = cv_img_raw.shape
        result_image = cv_img_raw.copy()
        cv_hsv_img = cv2.cvtColor(cv_img_raw, cv2.COLOR_BGR2HSV)  # Fix to BGR

        for hsv in HSV_RANGES.values():
            mask_img = hsv.apply_mask(hsv_image=cv_hsv_img)
            overexposed_mask_img = cv2.inRange(cv_hsv_img, (0, 0, 205), (255, 60, 255))

            color_contours, _ = cv2.findContours(mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            overexposed_contours, _ = cv2.findContours(overexposed_mask_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            self.pub_mask_img(mask_img=mask_img)


            for overexposed_contour in overexposed_contours:
                if self.is_connected_to_color(overexposed_contour, color_contours):
                    self.restore_overexposed_area(overexposed_contour, mask_img, result_image, height, width)

        return result_image

    def is_connected_to_color(self, overexposed_contour, color_contours):
        """Check if an overexposed contour is connected to any color contour."""
        for color_contour in color_contours:
            for point in overexposed_contour:
                pt = (int(point[0][0]), int(point[0][1]))
                if cv2.pointPolygonTest(color_contour, pt, False) >= 0:
                    return True
        return False

    def restore_overexposed_area(self, overexposed_contour, mask_img, result_image, height, width):
        """Restore the overexposed areas in the result image based on nearby color contours."""
        overexposed_area_mask = np.zeros((height, width), dtype=np.uint8)

        cv2.drawContours(overexposed_area_mask, [overexposed_contour], -1, 255, thickness=cv2.FILLED)

        self.pub_overexposed_mask_img(overexposed_mask_img=overexposed_area_mask)

        for y, x in zip(*np.where(overexposed_area_mask > 0)):
            for dy in range(-5, 6):
                for dx in range(-5, 6):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width and mask_img[ny, nx] > 0:
                        result_image[y, x] = [255, 0, 0]  # Mark as red
                        break

    def pub_cv_img(self, cv_img):
        self.publish_image(cv_img, self.cv_image_pub)

    def pub_result_cv_img(self, result_cv_img):
        self.publish_image(result_cv_img, self.result_cv_image_pub)

    def pub_overexposed_mask_img(self, overexposed_mask_img):
        self.publish_image(overexposed_mask_img, self.overexposed_mask_image_pub, encoding="passthrough")

    def pub_mask_img(self, mask_img):
        self.publish_image(mask_img, self.mask_image_pub, encoding="passthrough")

    def publish_image(self, cv_img, publisher, encoding="bgr8"):
        cv_img_msg = self.bridge.cv2_to_imgmsg(cv_img, encoding=encoding)
        cv_img_msg.header.stamp = rospy.Time.now()
        publisher.publish(cv_img_msg)

    def adjust_gamma(self, cv_img, gamma=1.0):
        invGamma = 1.0 / gamma
        lookup_table = np.array([(i / 255.0) ** invGamma * 255 for i in range(256)]).astype("uint8")
        adjusted_img = cv2.LUT(cv_img, lookup_table)

        # hsv_img = cv2.cvtColor(adjusted_img, cv2.COLOR_BGR2HSV)
        # white_mask = HSV_RANGES['white'].apply_mask(hsv_image=hsv_img)
        # self.pub_mask_img(mask_img=white_mask)
        # adjusted_img[white_mask > 0] = cv2.add(adjusted_img[white_mask > 0], (50, 50, 50))

        result_img = cv2.convertScaleAbs(adjusted_img, alpha=1.2, beta=30)
        
        return result_img

if __name__ == '__main__':
    try:
        image_processor_node = ImageProcessor()
        rospy.spin()  # Keep the node running, processing callbacks
    except rospy.ROSInterruptException:
        pass