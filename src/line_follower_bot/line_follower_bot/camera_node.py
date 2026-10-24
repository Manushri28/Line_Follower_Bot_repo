import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image as CameraImage
from std_msgs.msg import Float32MultiArray as LineOffsets

BANDS = ((0.50, 0.70), (0.30, 0.50), (0.10, 0.30))
MIN_PIXELS = 15

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.bridge = CvBridge()
        self.pub = self.create_publisher(LineOffsets, 'line_offsets', 10)
        self.create_subscription(CameraImage, 'camera/image_raw', self.process_image, 10)

    def process_image(self, image):
        gray = cv2.cvtColor(self.bridge.imgmsg_to_cv2(image, 'bgr8'), cv2.COLOR_BGR2GRAY)
        mask = cv2.GaussianBlur(gray, (5, 5), 0) < 128
        image_height, image_width = mask.shape
        offsets, previous_offset, previous_change, previous_band = [], 0.0, 0.0, 0
        for band, (top, bottom) in enumerate(BANDS):
            roi = mask[int(image_height * top):int(image_height * bottom)]
            columns = np.where(roi.sum(axis=0) >= 2)[0]
            segments = np.split(columns, np.flatnonzero(np.diff(columns) > 1) + 1)
            segments = [s for s in segments if roi[:, s].sum() >= MIN_PIXELS]
            if segments:
                band_gap = band - previous_band
                predicted = previous_offset + previous_change * band_gap
                predicted_x = (predicted + 1) * image_width / 2
                segment = min(segments, key=lambda s: abs(s.mean() - predicted_x))
                offset = (segment.mean() - image_width / 2) / (image_width / 2)
                if band_gap: previous_change = (offset - previous_offset) / band_gap
                previous_offset, previous_band = offset, band
                offsets.append(offset)
            else:
                offsets.append(float('nan'))
        self.pub.publish(LineOffsets(data=offsets))

def main():
    rclpy.init()
    rclpy.spin(CameraNode())

if __name__ == '__main__':
    main()
