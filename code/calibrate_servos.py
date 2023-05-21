import machine

servo = machine.PWM(machine.Pin(4, machine.Pin.OUT))
servo.freq(50)
servo.duty_u16(5000)
servo = machine.PWM(machine.Pin(5, machine.Pin.OUT))
servo.freq(50)
servo.duty_u16(5000)
servo = machine.PWM(machine.Pin(6, machine.Pin.OUT))
servo.freq(50)
servo.duty_u16(5000)
servo = machine.PWM(machine.Pin(7, machine.Pin.OUT))
servo.freq(50)
servo.duty_u16(5000)
