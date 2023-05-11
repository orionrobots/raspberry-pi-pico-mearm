from microdot_asyncio import Microdot
from connect import wifi_connect
from mearm import Arm
import uasyncio

app = Microdot()

@app.route('/')
async def index(request):
    print("Handling /")
    with open("control.html") as content:
        return content.read(), 200, {'Content-Type': 'text/html'}

@app.route('/open')
async def _open(request):
    uasyncio.create_task(Arm.grip.move(Arm.grip.min_position))
    return 'Opening'
    
@app.route('/close')
async def _close(request):
    uasyncio.create_task(Arm.grip.move(Arm.grip.max_position))
    return 'Closing'

@app.route('/set_base/<int:position>')
async def _set_base(request, position):
    uasyncio.create_task(Arm.base.move(position))
    return 'Moving'

@app.route('/set_shoulder/<int:position>')
async def _set_shoulder(request, position):
    uasyncio.create_task(Arm.shoulder.move(position))
    return 'Moving'

@app.route('/set_elbow/<int:position>')
async def _set_elbow(request, position):
    uasyncio.create_task(Arm.elbow.move(position))
    return 'Moving'

@app.route('/move_to/<int:x>/<int:y>/<int:z>')
async def _move_to(request, x, y, z):
    uasyncio.create_task(Arm.move_to(x, y, z))
    return 'Moving'

try:
    wifi_connect()
    print("Starting app")
    app.run(port=80)
except KeyboardInterrupt:
    machine.reset()
