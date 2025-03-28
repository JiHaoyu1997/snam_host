import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from sensor_msgs.msg import CameraInfo

def camera_info_callback(msg):
    global fx
    fx = msg.K[0]  # 获取相机内参矩阵的 fx（焦距）
    rospy.loginfo(f"Camera fx: {fx}")

def tag_detections_callback(msg):
    global fx
    if fx is None:
        rospy.logwarn("Waiting for camera info to get fx value...")
        return
    
    for detection in msg.detections:
        tag_id = detection.id[0]  # 获取 Tag ID
        Z = detection.pose.pose.pose.position.z  # AprilTag 到相机的距离（m）
        tag_size = 0.12  # 你需要设置 AprilTag 真实尺寸 (单位：m)
        tag_width_pixels = detection.size[0]  # AprilTag 在图像中的宽度 (像素)
        
        if tag_width_pixels > 0:
            pixel_size = tag_size / tag_width_pixels  # 计算每个像素的大小（m/pixel）
            rospy.loginfo(f"Tag {tag_id}: Distance Z={Z:.3f}m, Pixel Size={pixel_size*1000:.3f}mm/pixel")
        else:
            rospy.logwarn(f"Tag {tag_id}: Invalid width detected!")

if __name__ == "__main__":
    rospy.init_node("apriltag_pixel_size_calculator", anonymous=True)
    
    fx = None  # 用于存储相机焦距
    
    rospy.Subscriber("/camera/camera_info", CameraInfo, camera_info_callback)
    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, tag_detections_callback)
    
    rospy.loginfo("Started AprilTag pixel size calculator...")
    rospy.spin()
