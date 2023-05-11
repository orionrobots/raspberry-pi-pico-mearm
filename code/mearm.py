"""
import sys
del sys.modules["mearm"]
import mearm
arm = mearm.SmoothArm()
# tests
arm.move(120, 150, 50)
arm.reset()
arm.gripper_position(mearm.grip_closed)
arm.gripper_position(mearm.grip_fully_open)
"""
import machine
import utime

def degrees_to_duty(angle):
    return int(1000 + (angle * 8000/180))


def set_angle(servo, angle):
    servo.duty_u16(degrees_to_duty(angle))

grip_closed = 157
grip_fully_open = 100

class SmoothArm:
    left_current = 90
    right_current = 90 # right servo got hot? did I go too high - or is it a broken servo?
    base_current = 90
    grip_current = 100
    
    left_lower = 30
    left_upper = 120
    right_lower = 50
    right_upper = 150
    
    def __init__(self):
        self.grip_servo = machine.PWM(machine.Pin(4, machine.Pin.OUT))
        self.left_servo = machine.PWM(machine.Pin(5, machine.Pin.OUT))
        self.right_servo = machine.PWM(machine.Pin(6, machine.Pin.OUT))
        self.base_servo = machine.PWM(machine.Pin(7, machine.Pin.OUT))
        self.left_servo.freq(50)
        self.grip_servo.freq(50)
        self.right_servo.freq(50)
        self.base_servo.freq(50)      
    
    def move(self, left_pos, right_pos, base_pos, seconds=1, steps=100):
        step_time = seconds/steps
        left_step = (left_pos - self.left_current)/steps
        right_step = (right_pos - self.right_current)/steps
        base_step = (base_pos - self.base_current)/steps
        
        for n in range(steps):
            set_angle(self.left_servo, self.left_current)
            set_angle(self.right_servo, self.right_current)
            set_angle(self.base_servo, self.base_current)
            self.left_current += left_step
            self.right_current += right_step
            self.base_current += base_step
            utime.sleep(seconds/steps)
    
    def gripper_position(self, position, seconds=1, steps=100):
        step_time = seconds/steps
        grip_step = (position - self.grip_current) / steps
        
        for n in range(steps):
            set_angle(self.grip_servo, self.grip_current)
            self.grip_current += grip_step
            utime.sleep(seconds/steps)

    def reset(self):
        self.move(90, 90, 90)
        self.gripper_position(grip_fully_open)
