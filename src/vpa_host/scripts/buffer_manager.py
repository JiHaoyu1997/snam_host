#! /usr/bin/env python3

import rospy

from robot.robot import find_id_by_robot_name

from sensor_msgs.msg import Image

from vpa_host.srv import AssignTask, AssignTaskRequest, AssignTaskResponse  

class BufferManager:
    # Properties
    def __init__(self) -> None:
        # Init ROS Node
        rospy.init_node('buffer_manager')

        # BUFFER_AERA Robot Info
        # TODO: sequence func
        self.robot_buffer_info = []

        # 
        self.test_mode = rospy.get_param('~test_mode', 'default')
        
        # Publishers

        # Subscribers

        # Servers
        task_assign_server = rospy.Service("/assgin_task_srv", AssignTask, self.assign_task_cb) 

        # ServiceProxy
        
        # Init Log
        rospy.loginfo('Buffer Manager is Online')


    # Methods
    def assign_task_cb(self, req: AssignTaskRequest) -> None:

        robot_id = find_id_by_robot_name(req.robot_name)

        if self.test_mode != 'default':
            test_task_list = self.test_mode_func()
        else:
            test_task_list = [6, 2, 5, 4, 3, 1, 2, 6]

        resp = AssignTaskResponse(task_list = test_task_list)

        rospy.loginfo(f"Assigned {req.robot_name} Task List")
        
        return resp
    
    def test_mode_func(self):
        if self.test_mode == 'left':
            return [6, 2, 5, 4, 3, 5, 2, 6]
    
if __name__ == '__main__':
    N = BufferManager()
    rospy.spin()
        