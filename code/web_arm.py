import machine
import uasyncio
import json

from microdot_asyncio import Microdot
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
step_list = []

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

@app.route('/add_step')
async def add_step(request):
    state = (arm.base.current, arm.shoulder.current, arm.elbow.current, arm.grip.current)
    step_list.append(state)
    return 'Added step'

async def run_steps():
    try:
        for step in step_list:
            await arm.move_together(*step, seconds=1)
    except:
        print("Steps were:", step_list)
        raise

@app.route('/run_steps')
async def handle_run_steps(request):
    uasyncio.create_task(run_steps())
    return 'Running steps'

@app.route('/save_steps')
async def handle_save_steps(request):
    with open("steps.json", "w") as f:
        json.dump(step_list, f)
    return 'Saved steps'

@app.route('/clear_steps')
async def handle_clear_steps(request):
    step_list.clear()
    return 'Cleared steps'

@app.route('/load_steps')
async def handle_load_steps(request):
    global step_list
    with open("steps.json") as f:
        step_list = json.load(f)
    return 'Loaded steps'

try:
    wifi_connect()
    print("Starting app")
    app.run(port=80)
except KeyboardInterrupt:
    machine.reset()
