import uasyncio
from mearm import arm
from smart_grippers import SmartGrippers, check_power, power_monitor

do = uasyncio.run

grippers = SmartGrippers(arm.arm)
