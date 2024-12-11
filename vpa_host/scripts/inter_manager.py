#!/usr/bin/env python3

import rospy

import threading
import numpy as np
from typing import List, Dict

from robot.robot import robot_dict, RobotInfo

from vpa_host.msg import RobotInfo as RobotInfoMsg
from vpa_host.msg import InterInfo as InterInfoMsg
from vpa_host.msg import KinematicDataArray
from vpa_host.srv import InterMng, InterMngRequest, InterMngResponse


class InterInfo:
    def __init__(self, inter_id=0):
        self.inter_id = inter_id  # 交叉路口ID
        self.robot_id_list = []  # 机器人ID列表
        self.robot_info: List[RobotInfo] = []  # RobotInfo实例列表

    def update_robot_id_list(self, robot_id: int):
        if robot_id in self.robot_id_list:
            self.robot_id_list.remove(robot_id)
        self.robot_id_list.append(robot_id)

    def update_robot_info_list(self, new_robot_info: RobotInfo):
        for existed_robot_info in self.robot_info:
            if existed_robot_info.robot_id == new_robot_info.robot_id:
                existed_robot_info.__dict__.update(new_robot_info.__dict__)        
        self.robot_info.append(new_robot_info)            


class InterManager:

    def __init__(self) -> None:
        rospy.init_node('inter_manager')

        # global info
        self.robot_info_dict: Dict[int, RobotInfo] = {}
        self.inter_info_dict: Dict[int, InterInfo] = {i: InterInfo(i) for i in range(1, 6)}
        self.inter_info_dict_lock = threading.Lock()

        # Publishers
        self.inter_info_pubs = {i: rospy.Publisher(f'inter_info/{i}', InterInfoMsg, queue_size=1) for i in range(1, 6)}

        # Subscribers
        self.subscribers = []
        self.kinematic_info_sub = rospy.Subscriber('/kinematic_info', KinematicDataArray, self.kinematic_info_cb)

        # Servers
        self.inter_mng_server = rospy.Service('/inter_mng_srv', InterMng, self.inter_mng_cb)

        rospy.loginfo('Intersection Manager is Online')

        self.init_robot_info_subs()

        # 定时广播交叉路口信息
        rospy.Timer(rospy.Duration(1 / 10), self.broadcast_inter_info)

    def init_robot_info_subs(self):
        for robot_id, robot_name in robot_dict.items():
            topic = f"/{robot_name}/robot_info"
            subscriber = rospy.Subscriber(topic, RobotInfoMsg, self.robot_info_cb, callback_args=robot_id)
            self.subscribers.append(subscriber)
        return

    def robot_info_cb(self, msg: InterInfoMsg, robot_id):
        """
        Update local robot_info_dict.
        """
        robot_info = RobotInfo.from_msg(msg)        
        self.robot_info_dict[robot_id] = robot_info
        with self.inter_info_dict_lock:
            self.update_local_inter_info(robot_id=robot_id, robot_info=robot_info)
        return
    
    def update_local_inter_info(self, robot_id, robot_info: RobotInfo):
        for inter_id, inter_info in self.inter_info_dict.items():
            if robot_id in inter_info.robot_id_list:
                inter_info.update_robot_info_list(robot_info)
                return

    def inter_mng_cb(self, req: InterMngRequest) -> InterMngResponse:
        """
        Handle update global inter_info requeset 
        """
        try:
            robot_id = req.robot_id
            last_inter_id = req.last_inter_id
            curr_inter_id = req.curr_inter_id
            rospy.loginfo(f'Robot {robot_dict[robot_id]} moving from Inter_{last_inter_id} to Inter_{curr_inter_id}')
            
            # 更新交叉路口信息
            with self.inter_info_dict_lock:
                success = self.update_global_inter_info(robot_id=robot_id, from_inter=last_inter_id, to_inter=curr_inter_id)

            # 构造响应
            if success:
                resp = InterMngResponse()
                resp.success = success
                resp.message = f'Entry successful' if success else f'Entry denied'
                return resp
            
        except Exception as e:
            rospy.logerr(f'Error processing request: {e}')
            resp = InterMngResponse()
            resp.success = False
            resp.message = f'Error: {str(e)}'
            return resp

    def update_global_inter_info(self, robot_id: int, from_inter: int, to_inter: int) -> bool:
        """
        Update global inter_info
        """
        try:            
            # 
            updated_robot_info = self.robot_info_dict[robot_id]

            # 从原交叉路口移除机器人
            if from_inter in self.inter_info_dict:
                inter_info = self.inter_info_dict[from_inter]
                if robot_id in inter_info.robot_id_list:
                    inter_info.robot_id_list.remove(robot_id)
                    inter_info.robot_info = [ info for info in inter_info.robot_info if info.robot_id != robot_id ]

            # 在新交叉路口添加机器人
            if to_inter in self.inter_info_dict:
                inter_info = self.inter_info_dict[to_inter]
                inter_info.update_robot_id_list(robot_id=robot_id)
                inter_info.update_robot_info_list(new_robot_info=updated_robot_info)
            
            # 
            rospy.loginfo(f'{robot_dict[robot_id]} removed from inter_{from_inter} & added to inter_{to_inter}')
            rospy.loginfo('Current intersection status:')
            for inter_id, info in self.inter_info_dict.items():
                if info.robot_id_list:
                    rospy.loginfo(f'Inter_{inter_id}: {[robot_dict[id] for id in info.robot_id_list]}')

            return True

        except Exception as e:
            rospy.logerr(f'Error updating intersection info: {e}')
            return False

    def broadcast_inter_info(self, event):
        """
        Broadcast inter_info/x
        """
        for inter_id, inter_info in self.inter_info_dict.items():               
            msg = InterInfoMsg()
            msg.inter_id = inter_info.inter_id
            msg.robot_id_list = inter_info.robot_id_list
            
            # 转换RobotInfo为消息格式
            msg.robot_info = [
                RobotInfoMsg(
                    robot_name=info.robot_name,
                    robot_id=info.robot_id,
                    robot_route=info.robot_route,
                    robot_v=info.robot_v,
                    robot_p=info.robot_p,
                    robot_coordinate = info.robot_coordinate,
                    robot_enter_time=info.robot_enter_time,
                    robot_enter_conflict=info.robot_enter_conflict,
                    robot_arrive_cp_time=info.robot_arrive_cp_time,
                    robot_exit_time=info.robot_exit_time
                ) for info in inter_info.robot_info
            ]
            
            # 发布消息
            if inter_id in self.inter_info_pubs:
                self.inter_info_pubs[inter_id].publish(msg)
        return
    
    def kinematic_info_cb(self, kinematic_data_msg: KinematicDataArray):
        """
        Annotation
        """
        pass


if __name__ == '__main__':
    T = InterManager()
    rospy.spin()