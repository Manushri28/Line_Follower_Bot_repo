from math import isfinite

import rclpy
from geometry_msgs.msg import Twist
from line_follower_bot.line_follower_controller import LineFollowerController
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray


class LineFollowerNode(Node):
    def __init__(self):
        super().__init__('line_follower_node')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Float32MultiArray, 'line_offsets', self.follow_line, 10)
        self.controller = LineFollowerController(
            speed=self.declare_parameter('max_linear', 0.2).value,
            kp=self.declare_parameter('kp', 0.45).value,
            ki=self.declare_parameter('ki', 0.02).value,
            kd=self.declare_parameter('kd', 0.04).value,
            max_angular=self.declare_parameter('max_angular', 0.35).value,
            weights=self.declare_parameter('offset_weights', [0.1, 0.25, 0.65]).value,
            preview_gain=self.declare_parameter('preview_gain', 0.8).value,
            open_end_recovery=self.declare_parameter('open_end_recovery', False).value,
        )
        self.last_image_time = self.get_clock().now()
        self.camera_stale = False
        self.line_lost = False
        self.create_subscription(Odometry, 'odom', self.controller.update_odometry, 10)
        self.create_timer(0.5, self.stop_if_camera_stale)

    def follow_line(self, message):
        command = Twist()
        now = self.get_clock().now()
        dt = (now - self.last_image_time).nanoseconds / 1e9
        self.last_image_time = now
        self.camera_stale = False
        offsets = [
            (value, weight, index)
            for index, (value, weight) in enumerate(zip(message.data, self.controller.weights))
            if isfinite(value)
        ]
        if offsets and (not self.line_lost or self.controller.can_reacquire(offsets)):
            command.linear.x, command.angular.z = self.controller.follow(offsets, dt)
            self.line_lost = False
        else:
            if not self.line_lost:
                self.get_logger().warning('Line missing; continuing last steering direction')
            self.line_lost = True
            command.linear.x, command.angular.z = self.controller.recover(dt)
        self.publisher.publish(command)

    def stop_if_camera_stale(self):
        if self.camera_stale:
            return
        elapsed = (self.get_clock().now() - self.last_image_time).nanoseconds / 1e9
        if elapsed >= 0.5:
            self.publisher.publish(Twist())
            self.camera_stale = True


def main():
    rclpy.init()
    rclpy.spin(LineFollowerNode())


if __name__ == '__main__':
    main()
