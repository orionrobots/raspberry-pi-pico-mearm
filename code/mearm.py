"""
import sys
del sys.modules["mearm"]
from mearm import Arm
# tests
import uasyncio

arm = mearm.Arm()
tasks = [
    uasyncio.create_task(arm.grip.move(120)),
    uasyncio.create_task(arm.base.move(120)),
    uasyncio.create_task(arm.shoulder.move(120)),
    uasyncio.create_task(arm.elbow.move(120)),
]
uasyncio.run(uasyncio.gather(*tasks))
# or

uasyncio.run(arm.move_together(base_angle=120, shoulder_angle=120, elbow_angle=120, grip_angle=120))
uasyncio.run(arm.reset())
"""

import machine
import uasyncio

PWM_MIN = 1000
PWM_MAX = 9000
PWM_RANGE = PWM_MAX - PWM_MIN
PWM_FREQ = 50
DEGREES_TO_PWM = PWM_RANGE / 180

class AsyncServo:
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
    def __init__(self, grip_pin=4, elbow_pin=5, shoulder_pin=6, base_pin=7):
        self.grip = AsyncServo(grip_pin, reset_position=100, min_position=100, max_position=157)
        self.elbow = AsyncServo(elbow_pin, min_position=0, max_position=150)
        self.shoulder = AsyncServo(shoulder_pin, min_position=0, max_position=145)
        self.base = AsyncServo(base_pin, min_position=30, max_position=150)

    async def move_together(self, base_angle=None, shoulder_angle=None, elbow_angle=None, grip_angle=None, seconds=1, steps=100):
        tasks = []
        if base_angle is not None:
            tasks.append(uasyncio.create_task(self.base.move(base_angle, seconds=seconds, steps=steps)))
        if shoulder_angle is not None:
            tasks.append(uasyncio.create_task(self.shoulder.move(shoulder_angle, seconds=seconds, steps=steps)))
        if elbow_angle is not None:
            tasks.append(uasyncio.create_task(self.elbow.move(elbow_angle, seconds=seconds, steps=steps)))
        if grip_angle is not None:
            tasks.append(uasyncio.create_task(self.grip.move(grip_angle, seconds=seconds, steps=steps)))
        await uasyncio.gather(*tasks)

    async def reset(self, seconds=1, steps=100):
        await self.move_together(base_angle=90, shoulder_angle=90, elbow_angle=90, grip_angle=100, seconds=seconds, steps=steps)

do = uasyncio.run
