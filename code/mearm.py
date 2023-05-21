"""
import sys
del sys.modules["mearm"]
from mearm import arm, do
# tests
import uasyncio

do(arm.move_together(base=120, shoulder=120, elbow=120, grip=120))
do(arm.reset())
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
    def __init__(self, elbow_pin=4, grip_pin=5, shoulder_pin=6, base_pint=7):
        self.grip = AsyncServo(grip_pin, reset_position=100, min_position=100, max_position=157)
        self.elbow = AsyncServo(elbow_pin, min_position=0, max_position=150)
        self.shoulder = AsyncServo(shoulder_pin, min_position=0, max_position=145)
        self.base = AsyncServo(base_pint, min_position=30, max_position=150)

    async def move_together(self, base=None, shoulder=None, elbow=None, grip=None, seconds=1, steps=100):
        tasks = []
        if base is not None:
            tasks.append(uasyncio.create_task(self.base.move(base, seconds=seconds, steps=steps)))
        if shoulder is not None:
            tasks.append(uasyncio.create_task(self.shoulder.move(shoulder, seconds=seconds, steps=steps)))
        if elbow is not None:
            tasks.append(uasyncio.create_task(self.elbow.move(elbow, seconds=seconds, steps=steps)))
        if grip is not None:
            tasks.append(uasyncio.create_task(self.grip.move(grip, seconds=seconds, steps=steps)))
        await uasyncio.gather(*tasks)


arm = Arm()
do = uasyncio.run
