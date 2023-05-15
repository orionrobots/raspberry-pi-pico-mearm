import uasyncio
from machine import Pin, I2C
from ina219 import INA219

i2c_bus = I2C(1, scl=Pin(27), sda=Pin(26))
SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS, i2c_bus)

ina.configure()

def check_power():
    print("Bus Voltage: %.3f V" % ina.voltage())
    print("Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())

class SmartGrippers:
    def __init__(self, arm) -> None:
        self.arm = arm

    async def open_(self):
        await self.arm.grip.move(130)

    async def close(self, debug=False, sleep_time=0.1, power_threshold=700, step_size=0.1):
        while ina.power() < power_threshold:
            self.arm.grip.current += step_size
            self.arm.grip.set_angle(self.arm.grip.current)
            uasyncio.sleep(sleep_time)
            if debug:
                print(ina.power(), ina.voltage())

async def power_monitor(sleep_time=0.2):
    while True:
        print(ina.voltage(), ina.current())
        uasyncio.sleep(sleep_time)
