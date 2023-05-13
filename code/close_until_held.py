import utime
import uasyncio
from machine import Pin, I2C

from mearm import Arm
from ina219 import INA219

i2c_bus = I2C(1, scl=Pin(27), sda=Pin(26))
SHUNT_OHMS = 0.1
ina = INA219(SHUNT_OHMS, i2c_bus)
arm = Arm()

ina.configure()

def check_power():
    print("Bus Voltage: %.3f V" % ina.voltage())
    print("Current: %.3f mA" % ina.current())
    print("Power: %.3f mW" % ina.power())

def open_grips():
    uasyncio.run(Arm.grip.move(130))

def close_grips():
    while ina.power() < 600:
        Arm.grip.current += .1
        Arm.grip.set_angle(Arm.grip.current)
        utime.sleep(0.05)
        print(ina.power(), ina.voltage())
    
def grip_cycle():
    print("Open")
    open_grips()
    utime.sleep(0.2)
    check_power()
    print("Close grips")
    close_grips()
    check_power()
    print("Hold position")
    utime.sleep(1)
    check_power()
