from imports import time
from definitions import *
class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0
        self.last_time = time.time()

    def compute(self, current_value):
        now = time.time()
        dt = now - self.last_time
        if dt <= 0:
            dt = 0.01

        error = self.setpoint - current_value

        P = self.Kp * error

        self.integral += error * dt
        I = self.Ki * self.integral

        derivative = (error - self.last_error) / dt
        D = self.Kd * derivative

        self.last_error = error
        self.last_time = now

        output = P + I + D

        # Защита от разгона интегральной компоненты
        if output > MAX_PID_OUTPUT:
            self.integral /= 2;
            
        # Ограничение выхода
        output = max(MIN_SLIDER, min(MAX_INFLOW_SLIDER, output))

        return output
