#! /usr/bin/env python3

import rospy

from robot.robot import find_id_by_robot_name
from task.task_dispatcher import TaskDispatcher

from sensor_msgs.msg import Image

from vpa_host.srv import AssignTask, AssignTaskRequest, AssignTaskResponse  

class BufferManager:
    # Properties
    def __init__(self) -> None:
        
        # Init ROS Node
        rospy.init_node('buffer_manager')

        # 
        self.task_dispatcher = TaskDispatcher()


        # BUFFER_AERA Robot Info
        self.robot_buffer_info = {}

        # 
        self.test_mode = rospy.get_param('~test_mode', 'default')

        # 
        
        # Publishers


        # Subscribers


        # Servers
        task_assign_server = rospy.Service("/assign_task_srv", AssignTask, self.assign_task_cb) 

        # ServiceProxy

        
        # Init Log
        rospy.loginfo('Buffer Manager is Online')


    # Methods
    def assign_task_cb(self, req: AssignTaskRequest) -> None:
        robot_name = req.robot_name
        
        if robot_name not in self.robot_buffer_info:
            self.robot_buffer_info[robot_name] = {'task_list': []}

        task_index, task_list = self.task_dispatcher.assign_task_list(test_mode=self.test_mode)
        self.robot_buffer_info[robot_name]['task_list'] = task_list
        resp = AssignTaskResponse(task_list = task_list)
        rospy.loginfo(f"Assigned {robot_name} Task List {task_index}: {task_list}")        
        return resp
        
if __name__ == '__main__':
    N = BufferManager()
    rospy.spin()        