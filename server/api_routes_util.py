import json
import pexpect
from config import config

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

class Device:
    mode_enum = {
        "colour": 0,
        "temperature": 1,
        "music": 2
    }

    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.on = False
        self.mode = mode_enum["colour"]
        self.colour = (0, 0, 0)
        self.temperature = 0
        self.brightness = 0

gatt = PExpectMock()
if config["linux"]:
    gatt = pexpect.spawn("gatttool -I")

device_register = dict()
resolved_macs = dict()

def register_device(mac, name):
    if mac in resolved_macs.keys():
        resolved_name = resolved_macs[mac]

        if resolved_name in device_register.keys():
            return device_register[resolved_name]

        del resolved_macs[resolved_name]

    resolved_macs[mac] = name
    device = Device(mac, name)
    device_register[name] = device
    return device

def get_device(mac):
    return register_device(mac, "Govee_Light_" + str(len(device_register)))
