"""
import sys
del sys.modules["mearm"]
from mearm import Arm
# tests
Arm.grip.move(120)
Arm.grip.reset()
Arm.base.move(120)
Arm.base.reset()
Arm.shoulder.move(120)
Arm.shoulder.reset()
Arm.elbow.move(120)
Arm.elbow.reset()
"""
import machine
import utime

PWM_MIN = 1000
PWM_MAX = 9000
PWM_RANGE = PWM_MAX - PWM_MIN
PWM_FREQ = 50
DEGREES_TO_PWM = PWM_RANGE / 180

class Servo:
    def __init__(self, pin, reset_position=90, min_position=0, max_position=180):
        self.pwm = machine.PWM(machine.Pin(pin, machine.Pin.OUT))
        self.pwm.freq(PWM_FREQ)
        self.current = self.reset_position = reset_position
        self.max_position = max_position
        self.min_position = min_position

    def degrees_to_duty(self, angle):
        return int(PWM_MIN + (angle * DEGREES_TO_PWM))

    def set_angle(self, angle):
        self.pwm.duty_u16(self.degrees_to_duty(angle))

    def move(self, position, seconds=1, steps=100):
        step_time = seconds/steps
        position = max(self.min_position, min(self.max_position, position))
        step_size = (position - self.current) / steps
        for n in range(steps):
            utime.sleep(step_time)
            self.set_angle(self.current)
            self.current += step_size

    def reset(self, seconds=1, steps=100):
        self.move(self.reset_position, seconds=seconds, steps=steps)

class Arm:
    def __init__(self, elbow_pin=4, grip_pin=5, shoulder_pin=6, base_pin=7):
        self.grip = Servo(grip_pin, reset_position=100, min_position=100, max_position=157)
        self.elbow = Servo(elbow_pin, min_position=0, max_position=150)
        self.shoulder = Servo(shoulder_pin, min_position=0, max_position=145)
        self.base = Servo(base_pin, min_position=30, max_position=150)

    def reset(self):
        self.grip.reset()
        self.elbow.reset()
        self.shoulder.reset()
        self.base.reset()
