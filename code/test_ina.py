# Derived from https://github.com/chrisb2/pyb_ina219/tree/master, adapted for Pico.
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
