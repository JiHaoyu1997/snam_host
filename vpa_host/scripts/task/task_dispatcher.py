#!/usr/bin/env python3

import rospy

import os
import csv

from vpa_demo.srv import AssignTask,AssignTaskRequest,AssignTaskResponse

# Currently this will import a preset task list for robots to perform
# Notably, we need to think about how the process can be real-time

class TaskDispatcher:
    
    def __init__(self, ) -> None:

        self.all_task_lists_dict    = {}
        self.task_assign_count      = 0
        self.task_total_count       = 0

        self.generate_all_task_lists()


    def generate_all_task_lists(self):
        real_path       = os.path.dirname(os.path.realpath(__file__))
        src_directory   = os.path.dirname(real_path)
        file_path       = os.path.join(src_directory, "csv", 'tasks.csv')
        file            = open(file_path,'r')
        data            = list(csv.reader(file, delimiter=","))
        file.close()

        for row in range(len(data)):
            if row == 0:
                continue
            else:
                _row_content    = data[row]
                _row_task_list  = _row_content[1:len(_row_content)]
                _task_list      = [int(i) for i in _row_task_list]
                
                self.all_task_lists_dict[row - 1] = _task_list

        self.task_total_count  = len(self.all_task_lists_dict)
        rospy.loginfo('generate all task lists to the server')
    
    def assign_task_list(self, test_mode: str = 'default') -> list:  
        if test_mode != 'default':
            return self.test_mode_func(test_mode)

        if self.task_assign_count == self.task_total_count:
            rospy.loginfo_once('No more tasks')
            return []
        
        self.task_assign_count += 1
        return self.all_task_lists_dict[self.task_assign_count - 1]
    
    def test_mode_func(self, test_mode):
        if test_mode == 'left':
            return [6, 2, 5, 3, 2, 5, 4, 3, 5, 4, 1, 3, 4, 1, 2, 3, 1, 2, 6]
        
        if test_mode == 'right':
            return [6, 2, 1, 3, 2, 1, 4, 3, 1, 4, 5, 3, 4, 5, 2, 3, 5, 2, 6]

        if test_mode == 'circle':
            return [6, 2, 5, 4, 1, 2, 3, 5, 2, 1, 4, 5, 2, 6]
        
        if test_mode == 'test':
            return [6, 2, 3, 4, 5, 3, 2, 6]
