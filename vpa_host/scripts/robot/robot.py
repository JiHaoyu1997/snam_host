from vpa_host.msg import RobotInfo as RobotInfoMsg

robot_dict = {
    1:'mingna',
    2:'vivian',
    6:'henry',
    7:'dorie',
    8:'luna',
    9:'robert',
    10:'fiona',
}

def find_id_by_robot_name(robot_name):
    return next((key for key, value in robot_dict.items() if value == robot_name), None)

class RobotInfo:
    def __init__(self, name="", robot_id=0, route=[0, 0, 0], v=0.0, p=0.0, coordinate=(0.0, 0.0), enter_time=0.0, enter_conflict=False, arrive_cp_time=0.0, exit_time=0.0):
        self.robot_name = name
        self.robot_id = robot_id
        self.robot_route = route
        self.robot_v = v
        self.robot_p = p
        self.robot_coordinate = coordinate
        self.robot_enter_time = enter_time
        self.robot_enter_conflict = enter_conflict
        self.robot_arrive_cp_time = arrive_cp_time
        self.robot_exit_time = exit_time

    def to_robot_info_msg(self):
        """
        Annotation
        """
        msg = RobotInfoMsg()
        msg.robot_name = self.robot_name
        msg.robot_id = self.robot_id
        msg.robot_route = self.robot_route
        msg.robot_v = self.robot_v
        msg.robot_p = self.robot_p
        msg.robot_coordinate = self.robot_coordinate
        msg.robot_enter_time = self.robot_enter_time
        msg.robot_enter_conflict = self.robot_enter_conflict
        msg.robot_arrive_cp_time = self.robot_arrive_cp_time
        msg.robot_exit_time = self.robot_exit_time
        return msg

    @classmethod
    def from_msg(cls, msg: RobotInfoMsg):
        """从ROS消息创建RobotInfo实例"""
        return cls(
            name            =msg.robot_name,
            robot_id        =msg.robot_id,
            route           =msg.robot_route,
            v               =msg.robot_v,
            p               =msg.robot_p,
            coordinate      =msg.robot_coordinate,
            enter_time      =msg.robot_enter_time,
            enter_conflict  =msg.robot_enter_conflict,
            arrive_cp_time  =msg.robot_arrive_cp_time,
            exit_time       =msg.robot_exit_time
        )