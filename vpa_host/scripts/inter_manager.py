#!/usr/bin/env python3

import rospy

import numpy as np
from typing import List, Dict

from robot.robot import robot_dict, find_id_by_robot_name

from vpa_host.msg import RobotInfo as RobotInfoMsg
from vpa_host.msg import InterInfo as InterInfoMsg
from vpa_host.srv import InterMng, InterMngRequest, InterMngResponse

class RobotInfo:
    def __init__(self, name="", id=0, a=0.0, v=0.0, p=0.0, enter_time=0.0, arrive_cp_time=0.0, exit_time=0.0):
        self.robot_name = name
        self.robot_id = id
        self.robot_a = a  # 加速度
        self.robot_v = v  # 速度
        self.robot_p = p  # 位置
        self.robot_enter_time = enter_time
        self.robot_arrive_cp_time = arrive_cp_time
        self.robot_exit_time = exit_time

    @classmethod
    def from_msg(cls, msg: RobotInfoMsg):
        """从ROS消息创建RobotInfo实例"""
        return cls(
            name=msg.robot_name,
            id=msg.robot_id,
            a=msg.robot_a,
            v=msg.robot_v,
            p=msg.robot_p,
            enter_time=msg.robot_enter_time,
            arrive_cp_time=msg.robot_arrive_cp_time,
            exit_time=msg.robot_exit_time
        )

class InterInfo:
    def __init__(self, inter=0):
        self.inter = inter  # 交叉路口ID
        self.robot_id_list = []  # 机器人ID列表
        self.robot_info = []  # RobotInfo实例列表

class InterManager:

    def __init__(self) -> None:
        # 初始化ROS节点
        rospy.init_node('inter_manager')

        # 初始化交叉路口信息
        self.inter_info_dict: Dict[int, InterInfo] = {i: InterInfo(i) for i in range(1, 6)}

        # Publishers
        # 为每个交叉路口创建一个publisher
        self.inter_info_pubs = {
            i: rospy.Publisher(f'inter_info/{i}', InterInfoMsg, queue_size=1)
            for i in range(1, 6)
        }

        # Servers
        self.inter_mng_server = rospy.Service('/inter_mng_srv', InterMng, self.inter_mng_cb)

        rospy.loginfo('Intersection Manager is Online')

        # 定时广播交叉路口信息
        rospy.Timer(rospy.Duration(1 / 10), self.broadcast_inter_info)

    def inter_mng_cb(self, req: InterMngRequest) -> InterMngResponse:
        """处理机器人的交叉路口管理请求"""
        try:
            rospy.loginfo(f'Received request from {req.robot_name}')
            rospy.loginfo(f'Robot {req.robot_name} moving from Inter_{req.last_inter_id} to Inter_{req.curr_inter_id}')

            # 将请求中的机器人信息转换为RobotInfo实例
            robot_info = RobotInfo.from_msg(req.robot_info)
            
            # 更新交叉路口信息
            success = self.update_inter_info(
                robot_info=robot_info,
                from_inter=req.last_inter_id,
                to_inter=req.curr_inter_id,
                timestamp=req.header.stamp
            )

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

    def update_inter_info(self, robot_info: RobotInfo, 
                         from_inter: int, to_inter: int, 
                         timestamp: rospy.Time) -> bool:
        """更新交叉路口信息"""
        try:
            # 从原交叉路口移除机器人
            if from_inter in self.inter_info_dict:
                inter_info = self.inter_info_dict[from_inter]
                if robot_info.robot_id in inter_info.robot_id_list:
                    inter_info.robot_id_list.remove(robot_info.robot_id)
                    inter_info.robot_info = [
                        info for info in inter_info.robot_info 
                        if info.robot_id != robot_info.robot_id
                    ]
                    rospy.loginfo(f'Removed {robot_info.robot_name} from inter_{from_inter}')

            # 在新交叉路口添加机器人
            if to_inter in self.inter_info_dict:
                inter_info = self.inter_info_dict[to_inter]
                if robot_info.robot_id not in inter_info.robot_id_list:
                    inter_info.robot_id_list.append(robot_info.robot_id)
                    robot_info.robot_enter_time = timestamp.to_sec()  # 更新进入时间
                    inter_info.robot_info.append(robot_info)
                    rospy.loginfo(f'Added {robot_info.robot_name} to inter_{to_inter}')
                else:
                    # 如果机器人已经在列表中，更新其信息
                    for i, info in enumerate(inter_info.robot_info):
                        if info.robot_id == robot_info.robot_id:
                            inter_info.robot_info[i] = robot_info
                            rospy.loginfo(f'Updated info for {robot_info.robot_name} in inter_{to_inter}')

            rospy.loginfo('Current intersection status:')
            for inter_id, info in self.inter_info_dict.items():
                if info.robot_id_list:
                    rospy.loginfo(f'Inter_{inter_id}: {[robot_dict[id] for id in info.robot_id_list]}')

            return True

        except Exception as e:
            rospy.logerr(f'Error updating intersection info: {e}')
            return False

    def broadcast_inter_info(self, event):
        """广播每个交叉路口的信息"""
        for inter_id, inter_info in self.inter_info_dict.items():
            if inter_id == 0:  # 跳过ID为0的交叉路口
                continue
                
            msg = InterInfoMsg()
            msg.inter_id = inter_id
            msg.robot_id_list = inter_info.robot_id_list
            
            # 转换RobotInfo为消息格式
            msg.robot_info = [
                RobotInfoMsg(
                    robot_name=info.robot_name,
                    robot_id=info.robot_id,
                    robot_a=info.robot_a,
                    robot_v=info.robot_v,
                    robot_p=info.robot_p,
                    robot_enter_time=info.robot_enter_time,
                    robot_arrive_cp_time=info.robot_arrive_cp_time,
                    robot_exit_time=info.robot_exit_time
                ) for info in inter_info.robot_info
            ]
            
            # 发布消息
            if inter_id in self.inter_info_pubs:
                self.inter_info_pubs[inter_id].publish(msg)

if __name__ == '__main__':
    T = InterManager()
    rospy.spin()