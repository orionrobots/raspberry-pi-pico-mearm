"""
import sys
del sys.modules["mearm"]
from mearm import Arm
# tests
import uasyncio
tasks = [
    Arm.grip.move(120),
    Arm.base.move(120),
    Arm.shoulder.move(120),
    Arm.elbow.move(120),
]
uasyncio.run(uasyncio.gather(tasks))
# or

uasyncio.run(Arm.move_together(base_angle=120, left_angle=120, right_angle=120, grip_angle=120))
"""

import machine
import uasyncio

PWM_MIN = 1000
PWM_MAX = 9000
PWM_RANGE = PWM_MAX - PWM_MIN
PWM_FREQ = 50

class AsyncServo:
    def __init__(self, pin, reset_position=90, min_position=0, max_position=180):
        self.pwm = machine.PWM(machine.Pin(pin, machine.Pin.OUT))
        self.pwm.freq(PWM_FREQ)
        self.current = self.reset_position = reset_position
        self.max_position = max_position
        self.min_position = min_position

    def degrees_to_duty(self, angle):
        return int(PWM_MIN + (angle * PWM_RANGE/180))

    def set_angle(self, angle):
        self.pwm.duty_u16(self.degrees_to_duty(angle))

    async def move(self, position, seconds=1, steps=100):
        step_time = seconds/steps
        position = max(self.min_position, min(self.max_position, position))
        step_size = (position - self.current) / steps
        for n in range(steps):
            await uasyncio.sleep(step_time)
            self.set_angle(self.current)
            self.current += step_size

    async def reset(self, seconds=1, steps=100):
        await self.move(self.reset_position, seconds=seconds, steps=steps)

class Arm:
    grip = AsyncServo(4, reset_position=100, min_position=100, max_position=157)
    left = AsyncServo(5, min_position=30, max_position=120)
    right = AsyncServo(6, min_position=50, max_position=150)
    base = AsyncServo(7, min_position=30, max_position=150)

    async def move_together(base_angle=None, shoulder_angle=None, elbow_angle=None, grip_angle=None, seconds=1, steps=100):
        tasks = []
        if base_angle is not None:
            tasks.append(Arm.base.move(base_angle, seconds=seconds, steps=steps))
        if shoulder_angle is not None:
            tasks.append(Arm.shoulder.move(shoulder_angle, seconds=seconds, steps=steps))
        if elbow_angle is not None:
            tasks.append(Arm.elbow.move(elbow_angle, seconds=seconds, steps=steps))
        if grip_angle is not None:
            tasks.append(Arm.grip.move(grip_angle, seconds=seconds, steps=steps))
        return uasyncio.gather(tasks)
