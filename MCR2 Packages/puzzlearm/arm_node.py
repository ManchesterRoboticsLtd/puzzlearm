import rclpy
from rclpy.node import Node
from rclpy import qos
from std_msgs.msg import Int32
from sensor_msgs.msg import JointState

from Arm_Lib import Arm_Device


class ArmJointMove(Node):
    def __init__(self):
        super().__init__('arm_joint_move')

        # publishers and subscribers
        self.sub_joints = self.create_subscription(JointState,'arm_joints_set',self.joints_cmd_callback,qos.qos_profile_sensor_data)
        self.arm_out_pub = self.create_publisher(JointState, 'arm_joints_enc', 10)

        # arm information
        self.Arm = Arm_Device()
        self.arm_joints_deg = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
        self.arm_cmd_deg = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
        self.new_pos = False

        # timer
        self.dt = 1
        self.timer = self.create_timer(self.dt, self.timer_callback)
        self.get_logger().info("Arm node started correclty")

        # start up information
        self.read_arm_joints()
        print(self.arm_joints_deg)
        
    def build_and_pub_cmd(self):
        msg = JointState()
        msg.name = ["joint 1", "joint 2", "joint 3", "joint 4", "joint 5", "joint 6"]
        msg.position = self.arm_cmd_deg
        self.arm_out_pub.publish(msg)

    def read_arm_joints(self):
        for i in range(1,7):
            comm_res = self.Arm.Arm_serial_servo_read(i)
            if comm_res != None:
                self.arm_joints_deg[i-1] = float(comm_res)
            self.build_and_pub_cmd()

    def joints_cmd_callback(self, msg): # desiered pos subscriber
        if len(msg.position) == 6:
            self.arm_cmd_deg = msg.position
            self.new_pos = True
            
    def shutdown_arm(self):
        self.Arm.Arm_serial_servo_write6_array([90, 90, 90, 90, 90, 90], 5000)
        self.Arm.Arm_serial_set_torque(0)

    #Timer Callback
    def timer_callback(self):
        
        # move the arm if there is a new msg
        if self.new_pos:
            dt_arm = self.dt*1000
            self.Arm.Arm_serial_servo_write6_array(self.arm_cmd_deg, dt_arm)
            self.new_pos = False
            self.get_logger().info("Moving the arm")

        self.read_arm_joints()
        


def main(args=None):
    rclpy.init(args=args)
    arm_node = ArmJointMove()
    try: rclpy.spin(arm_node)
    except KeyboardInterrupt: arm_node.shutdown_arm()
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        arm_node.destroy_node() 


if __name__ == '__main__':
    main()

