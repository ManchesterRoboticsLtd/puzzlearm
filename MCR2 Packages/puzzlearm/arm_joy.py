#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy, JointState # Importa el tipo de mensaje oficial para controles

class JoyController(Node):

    def __init__(self):
        super().__init__('xbox_controller_reader')
        
        # Nos suscribimos al topic '/joy' que genera el paquete oficial de ROS2
        self.control_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.arm_sub = self.create_subscription(JointState, 'arm_joints_enc', self.arm_joints_callback, 10)
        self.arm_cmd_pub = self.create_publisher(JointState, 'arm_joints_set', 10)

        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info('Arm with Xbox Controller Started')
        self.arm_cmd_deg = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
        self.arm_joints_deg = [90, 90, 90, 90, 90, 90]

    def arm_joints_callback(self, msg):
        if len(msg.position) == 6:
            self.arm_joints_deg = msg.position

    def build_and_pub_cmd(self):
        msg = JointState()
        msg.name = ["joint 1", "joint 2", "joint 3", "joint 4", "joint 5", "joint 6"]
        msg.position = self.arm_cmd_deg
        self.arm_cmd_pub.publish(msg)

    def joy_callback(self, msg):

        # Los rangos van de -1.0 a 1.0
        Astk_x = msg.axes[0]  # Izquierda (+) / Derecha (-)
        Astk_y = msg.axes[1]  # Arriba (+) / Abajo (-)
        
        Bstk_y = msg.axes[7]  # D-Pad Arriba (1.0) / Abajo (-1.0)

        Cstk_x = msg.axes[3]  # Izquierda (+) / Derecha (-)
        Cstk_y = msg.axes[4]  # Arriba (+) / Abajo (-)

        Gd = msg.axes[5]  # Suelto (1.0) / Presionado al fondo (-1.0)
        Gi = msg.axes[2]  # Suelto (1.0) / Presionado al fondo (-1.0)
        
        step = 4

        # JOY A
        if Astk_x == 0: pass
        else: self.arm_cmd_deg[0] = float(min(180, max(0,self.arm_joints_deg[0] + step*Astk_x / abs(Astk_x))))

        if Astk_y == 0: pass
        else: self.arm_cmd_deg[2] = float(min(180, max(0,self.arm_joints_deg[2] + step*Astk_y / abs(Astk_y))))

        # JOY B
        if Bstk_y == 0: pass
        else: self.arm_cmd_deg[1] = float(min(180, max(0,self.arm_joints_deg[1] + step*Bstk_y / abs(Bstk_y))))

        # JOY C
        if Cstk_x == 0: pass
        else: self.arm_cmd_deg[4] = float(min(180, max(0,self.arm_joints_deg[4] + step*Cstk_x / abs(Cstk_x))))
        
        if Cstk_y == 0: pass
        else: self.arm_cmd_deg[3] = float(min(180, max(0,self.arm_joints_deg[3] + step*Cstk_y / abs(Cstk_y))))

        # G
        if Gi < 0: self.arm_cmd_deg[5] = float(min(180, max(0,self.arm_joints_deg[5] - 2*step)))
        if Gd < 0: self.arm_cmd_deg[5] = float(min(180, max(0,self.arm_joints_deg[5] + 2*step)))


    def timer_callback(self):
        print(self.arm_cmd_deg)
        self.build_and_pub_cmd()

def main(args=None):
    rclpy.init(args=args)
    xbox_control = JoyController()
    try:
        rclpy.spin(xbox_control)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()
        xbox_control.destroy_node()


if __name__ == '__main__':
    main()
