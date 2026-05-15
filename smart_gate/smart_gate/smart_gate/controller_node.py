import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String

class ControllerNode(Node):
    def __init__(self):
        super().__init__('controller_node')
        # 거리를 듣고(Subscribe), 모터에 명령(Publish) 보냄
        self.subscription = self.create_subscription(Int32, 'distance', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(String, 'gate_command', 10)

    def listener_callback(self, msg):
        cmd = String()
        if msg.data < 15: # 거리가 15cm보다 가까우면
            cmd.data = 'OPEN'
        else:
            cmd.data = 'CLOSE'
        self.publisher_.publish(cmd)
        self.get_logger().info(f'판단 결과: {cmd.data}')

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()