from microdot_asyncio import Microdot
from connect import wifi_connect


app = Microdot()

@app.route('/')
async def index(request):
    print("Handling /")
    with open("control.html") as content:
        return content.read(), 200, {'Content-Type': 'text/html'}

try:
    wifi_connect()
    print("Starting app")
    app.run(port=80)
except KeyboardInterrupt:
    machine.reset()
