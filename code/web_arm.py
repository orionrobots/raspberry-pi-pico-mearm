import machine
import uasyncio

from microdot_asyncio import Microdot
from connect import wifi_connect
from mearm import Arm

import network
from utime import sleep

from secrets import *

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PSK)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

app = Microdot()
arm = Arm()

@app.route('/')
async def index(request):
    with open("control.html") as content:
        return content.read(), 200, {'Content-Type': 'text/html'}

@app.route('/set_grip/<position>')
async def set_base(request, position):
    uasyncio.create_task(arm.grip.move(int(position)))
    return 'Moving'

@app.route('/set_base/<position>')
async def set_base(request, position):
    uasyncio.create_task(arm.base.move(int(position)))
    return 'Moving'

@app.route('/set_shoulder/<position>')
async def set_shoulder(request, position):
    uasyncio.create_task(arm.shoulder.move(int(position)))
    return 'Moving'

@app.route('/set_elbow/<position>')
async def set_elbow(request, position):
    uasyncio.create_task(arm.elbow.move(int(position)))
    return 'Moving'

try:
    wifi_connect()
    print("Starting app")
    app.run(port=80)
except KeyboardInterrupt:
    machine.reset()
