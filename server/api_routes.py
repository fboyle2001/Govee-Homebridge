from flask import request, Flask
import json
import bluetooth_controller as controller

class PExpectMock:
    def sendline(self, data):
        return True

    def expect(self, data, timeout=100):
        return True

class APIResponse:
    default_messages = {
        200: "Success",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        410: "Gone",
        500: "Internal Server Error"
    }

    def __init__(self, code = None, message = None):
        if code == None:
            self.status = dict()
        else:
            self.set_status(code, message)

        self.data = dict()

    def set_status(self, code, message = None):
        self.status = {
            "code": code,
            "message": self.default_messages[code] if message == None else message
        }

    def add_data(self, key, value):
        self.data[key] = value

    def set_data(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self, default = lambda k: k.__dict__, sort_keys = True, indent = 2)

app = Flask(__name__)
gatt = PExpectMock() #Windows
#import pexpect
#gatt = pexpect.spawn("gatttool -I")

@app.route("/brightness")
def change_brightness():
    response = APIResponse()

    device = request.args.get("device")
    level = request.args.get("level")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if level == None:
        response.set_status(400, "Missing brightness level")
        return response.to_json()
    else:
        try:
            level = int(level)
        except ValueError:
            response.set_status(400, "level must be an integer between 0 and 255")
            return response.to_json()

        if level < 0 or level > 255:
            response.set_status(400, "level must be an integer between 0 and 255")
            return response.to_json()

    packet = controller.GoveePacket.brightness_packet(level)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
    else:
        response.set_status(400, "Unable to connect to device")

    return response.to_json()

@app.route("/colour")
def change_colour():
    response = APIResponse()

    device = request.args.get("device")
    r = request.args.get("r")
    g = request.args.get("g")
    b = request.args.get("b")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if r == None:
        r = 0
    else:
        try:
            r = int(r)
        except ValueError:
            response.set_status(400, "r must be an integer between 0 and 255")
            return response.to_json()

        if r < 0 or r > 255:
            response.set_status(400, "r must be an integer between 0 and 255")
            return response.to_json()

    if g == None:
        g = 0
    else:
        try:
            g = int(g)
        except ValueError:
            response.set_status(400, "g must be an integer between 0 and 255")
            return response.to_json()

        if g < 0 or g > 255:
            response.set_status(400, "g must be an integer between 0 and 255")
            return response.to_json()

    if b == None:
        b = 0
    else:
        try:
            b = int(b)
        except ValueError:
            response.set_status(400, "b must be an integer between 0 and 255")
            return response.to_json()

        if b < 0 or b > 255:
            response.set_status(400, "b must be an integer between 0 and 255")
            return response.to_json()

    packet = controller.GoveePacket.rgb_packet(r, g, b)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
    else:
        response.set_status(400, "Unable to connect to device")

    return response.to_json()
