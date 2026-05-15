import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import lgpio
import time

class StepperNode(Node):
    def __init__(self):
        super().__init__('stepper_node')
        self.subscription = self.create_subscription(String, 'gate_command', self.listener_callback, 10)
        
        # BCM 핀 번호 설정
        self.pins = [17, 18, 27, 22]
        
        # GPIO 칩 열기 (라즈베리 파이 5 대응)
        try:
            self.h = lgpio.gpiochip_open(0)
            for pin in self.pins:
                lgpio.gpio_claim_output(self.h, pin)
            self.get_logger().info('=== 라즈베리 파이 5 하드웨어 연결 성공! ===')
        except Exception as e:
            self.get_logger().error(f'GPIO 초기화 실패: {e}')

    def listener_callback(self, msg):
        if msg.data == 'OPEN' or msg.data == 'CLOSE':
            self.get_logger().info(f'[{msg.data}] 신호 수신 - 모터를 구동합니다.')
            self.move_stepper()

    def move_stepper(self):
        # 1-2상 여자 방식 (부드럽고 힘이 좋음)
        seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0], 
               [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]
        
        # 약 512번 반복하면 한 바퀴 정도 돕니다. 시연용으로 128정도만 줄게요.
        for _ in range(128):
            for step in seq:
                for i in range(4):
                    lgpio.gpio_write(self.h, self.pins[i], step[i])
                time.sleep(0.001) # 속도 조절 (너무 빠르면 탈조 발생)
        
        # 회전 후 모든 핀 끄기 (과열 방지)
        for pin in self.pins:
            lgpio.gpio_write(self.h, pin, 0)

def main(args=None):
    rclpy.init(args=args)
    node = StepperNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'h'):
            lgpio.gpiochip_close(node.h)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()