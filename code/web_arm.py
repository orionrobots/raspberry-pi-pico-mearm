import machine
import uasyncio

from microdot_asyncio import Microdot
from connect import wifi_connect
from mearm import Arm, IKArm
from smart_grippers import SmartGrippers

app = Microdot()
arm = Arm()
ik_arm = IKArm(arm)
grippers = SmartGrippers(arm)

@app.route('/')
async def index(request):
    print("Handling /")
    with open("control.html") as content:
        return content.read(), 200, {'Content-Type': 'text/html'}

@app.route('/open')
async def _open(request):
    uasyncio.create_task(grippers.open_grippers())
    return 'Opening'
    
@app.route('/close')
async def _close(request):
    uasyncio.create_task(grippers.close_grippers())
    return 'Closing'

@app.route('/set_base/<int:position>')
async def _set_base(request, position):
    uasyncio.create_task(arm.base.move(position))
    return 'Moving'

@app.route('/set_shoulder/<int:position>')
async def _set_shoulder(request, position):
    uasyncio.create_task(arm.shoulder.move(position))
    return 'Moving'

@app.route('/set_elbow/<int:position>')
async def _set_elbow(request, position):
    uasyncio.create_task(arm.elbow.move(position))
    return 'Moving'

@app.route('/move_to/<int:x>/<int:y>/<int:z>')
async def _move_to(request, x, y, z):
    uasyncio.create_task(ik_arm.move_to(x, y, z))
    return 'Moving'

try:
    wifi_connect()
    print("Starting app")
    app.run(port=80)
except KeyboardInterrupt:
    machine.reset()
