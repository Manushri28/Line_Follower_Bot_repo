import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image as CameraImage
from std_msgs.msg import Float32MultiArray as LineOffsets

BANDS = ((0.50, 0.70), (0.30, 0.50), (0.10, 0.30))
MIN_PIXELS = 15
TURN_SIDE = -1   # -1: track turns left (counter-clockwise), +1: turns right
WIDE = 1.6       # segment this many times wider than a normal line = merged crossing

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.bridge = CvBridge()
        self.width_ref = [None] * len(BANDS)
        self.pub = self.create_publisher(LineOffsets, 'line_offsets', 10)
        self.create_subscription(CameraImage, 'camera/image_raw', self.process_image, 10)

    def pick(self, band, segments):
        ref = self.width_ref[band]
        wide = ref is not None and max(len(s) for s in segments) > WIDE * ref
        if len(segments) == 1 and not wide:
            s = segments[0]
            self.width_ref[band] = len(s) if ref is None else 0.95 * ref + 0.05 * len(s)
            return s.mean(), False
        if len(segments) > 1:
            return segments[0 if TURN_SIDE < 0 else -1].mean(), True
        s = segments[0]
        return (s[0] + ref / 2 if TURN_SIDE < 0 else s[-1] - ref / 2), True

    def process_image(self, image):
        gray = cv2.cvtColor(self.bridge.imgmsg_to_cv2(image, 'bgr8'), cv2.COLOR_BGR2GRAY)
        mask = cv2.GaussianBlur(gray, (5, 5), 0) < 128
        image_height, image_width = mask.shape
        offsets, level = [], 0
        for band, (top, bottom) in enumerate(BANDS):
            roi = mask[int(image_height * top):int(image_height * bottom)]
            columns = np.where(roi.sum(axis=0) >= 2)[0]
            segments = np.split(columns, np.flatnonzero(np.diff(columns) > 1) + 1)
            segments = [s for s in segments if roi[:, s].sum() >= MIN_PIXELS]
            if segments:
                x, junction = self.pick(band, segments)
                level += junction
                offsets.append((x - image_width / 2) / (image_width / 2))
            else:
                offsets.append(float('nan'))
        self.pub.publish(LineOffsets(data=offsets + [float(level)]))

def main():
    rclpy.init()
    rclpy.spin(CameraNode())

if __name__ == '__main__':
    main()