from math import atan2, cos, pi, sin

OPEN_END_DELAY, TURNAROUND_MARGIN, RECOVERY_TURN, RECOVERY_SWEEP = 1.5, 0.15, 0.4, 1.5


class LineFollowerController:
    def __init__(self, speed, kp, ki, kd, max_angular, weights, preview_gain, open_end_recovery):
        self.speed, self.kp, self.ki, self.kd = speed, kp, ki, kd
        self.max_angular, self.weights = max_angular, weights
        self.preview_gain, self.open_end_recovery = preview_gain, open_end_recovery
        self.previous_error, self.integral, self.recovery_direction = 0.0, 0.0, 1.0
        self.yaw, self.lost_time, self.turnaround_yaw, self.turned_around = 0.0, 0.0, None, False

    def follow(self, offsets, dt):
        self.lost_time, self.turnaround_yaw, self.turned_around = 0.0, None, False
        total_weight = sum(weight for _, weight, _ in offsets)
        weighted_error = sum(value * weight for value, weight, _ in offsets) / total_weight
        nearest_error = min(offsets, key=lambda offset: offset[2])[0]
        preview = self.preview_gain * max(0.0, 1 - abs(weighted_error - nearest_error) / 0.3)
        error = (1 - preview) * nearest_error + preview * weighted_error
        self.integral = max(-1.0, min(1.0, self.integral + error * dt))
        derivative = max(-3.0, min(3.0, (error - self.previous_error) / dt)) if dt > 0 else 0.0
        turn = -(self.kp * error + self.ki * self.integral + self.kd * derivative)
        angular = max(-self.max_angular, min(self.max_angular, turn))
        self.previous_error = error
        if abs(angular) > 0.05: self.recovery_direction = 1.0 if angular > 0 else -1.0
        return self.speed, angular

    def update_odometry(self, message):
        q = message.pose.pose.orientation
        self.yaw = atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y**2 + q.z**2))

    def can_reacquire(self, offsets):
        if self.open_end_recovery or len(offsets) < 2:
            return self.open_end_recovery
        error = sum(value * weight for value, weight, _ in offsets)
        return self.recovery_direction * -error >= 0.0

    def recover(self, dt):
        self.integral = 0.0
        self.lost_time += max(0.0, dt)
        if not self.open_end_recovery:
            if self.turnaround_yaw is None: self.turnaround_yaw = self.yaw
            delta = self.yaw - self.turnaround_yaw
            angle = atan2(sin(delta), cos(delta))
            turn_progress = self.recovery_direction * angle
            if turn_progress >= RECOVERY_SWEEP: return 0.0, 0.0
            return 0.0, self.recovery_direction * min(self.max_angular, RECOVERY_TURN)
        if self.lost_time < OPEN_END_DELAY:
            return self.speed, self.recovery_direction * min(self.max_angular, RECOVERY_TURN)
        if self.turned_around: return self.speed, 0.0
        if self.turnaround_yaw is None:
            self.turnaround_yaw = self.yaw
        angle = atan2(sin(self.yaw - self.turnaround_yaw), cos(self.yaw - self.turnaround_yaw))
        if self.recovery_direction * angle >= pi - TURNAROUND_MARGIN:
            self.turned_around = True
            return self.speed, 0.0
        return 0.0, self.recovery_direction * self.max_angular
