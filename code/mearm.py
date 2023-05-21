"""
import sys
del sys.modules["mearm"]
from mearm import arm, do
# tests

do(arm.move_together(base=30, shoulder=40, elbow=30, grip=20))
do(arm.move_together(shoulder=0, elbow=-30))
"""
import machine
import uasyncio


PWM_MID = 5000
PWM_FREQ = 50
DEGREES_TO_PWM = 4000 / 90


class AsyncServo:
    def __init__(self, pin):
        self.pwm = machine.PWM(machine.Pin(pin, machine.Pin.OUT))
        self.pwm.freq(PWM_FREQ)
        self.current = 0

    def set_angle(self, angle):
        self.pwm.duty_u16(int(PWM_MID + (angle * DEGREES_TO_PWM)))

    async def move(self, position, seconds=1, steps=100):
        step_time = seconds/steps
        step_size = (position - self.current) / steps
        for n in range(steps):
            await uasyncio.sleep(step_time)
            self.set_angle(self.current)
            self.current += step_size


class Arm:
    def __init__(self, elbow_pin=4, grip_pin=5, shoulder_pin=6, base_pin=7):
        self.grip = AsyncServo(grip_pin)
        self.elbow = AsyncServo(elbow_pin)
        self.shoulder = AsyncServo(shoulder_pin)
        self.base = AsyncServo(base_pin)

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
