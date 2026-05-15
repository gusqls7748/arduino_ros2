import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
import serial
import time

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        
        # 1. 아두이노 시리얼 포트 연결
        # /dev/ttyACM0가 기본이나, 안될 경우 /dev/ttyUSB0 시도
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
            self.get_logger().info('아두이노 연결 성공! (/dev/ttyACM0)')
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
                self.get_logger().info('아두이노 연결 성공! (/dev/ttyUSB0)')
            except Exception as e:
                self.get_logger().error(f'아두이노 연결 실패: {e}')

        # 2. 토픽 발행 및 구독 설정
        # 거리는 기존처럼 Int32로 발행 (controller_node와 호환)
        self.publisher_ = self.create_publisher(Int32, 'distance', 10)
        self.subscription = self.create_subscription(String, 'gate_command', self.listener_callback, 10)
        
        # 3. 0.1초마다 아두이노 데이터 확인을 위한 타이머
        self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        # 아두이노에서 보낸 데이터(거리,온도,습도,조도) 읽기
        if hasattr(self, 'ser') and self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                # 콤마(,)를 기준으로 데이터 분리
                data = line.split(',')
                
                if len(data) == 4:
                    dist = data[0]
                    temp = data[1]
                    humi = data[2]
                    light = data[3]
                    
                    # 거리 데이터 발행 (컨트롤러 노드 전달용)
                    msg = Int32()
                    msg.data = int(dist)
                    self.publisher_.publish(msg)
                    
                    # 터미널에 모든 센서 값 출력 (교수님 확인용)
                    self.get_logger().info(f'[데이터] 거리:{dist}cm | 온도:{temp}°C | 습도:{humi}% | 조도:{light}')
                
            except Exception as e:
                # 데이터 파싱 에러 방지
                pass

    def listener_callback(self, msg):
        # 컨트롤러 노드에서 온 'OPEN'/'CLOSE' 명령을 아두이노로 전달
        if hasattr(self, 'ser'):
            if msg.data == 'OPEN':
                self.ser.write(b'O')
                self.get_logger().info('>>> 아두이노로 OPEN 명령 전송')
            elif msg.data == 'CLOSE':
                self.ser.write(b'C')
                self.get_logger().info('>>> 아두이노로 CLOSE 명령 전송')

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(node, 'ser'):
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()