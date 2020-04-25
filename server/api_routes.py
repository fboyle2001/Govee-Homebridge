from flask import request, Flask
import bluetooth_controller as controller
from api_routes_util import *

app = Flask(__name__)

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
        get_device(device).brightness = level
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
        get_device(device).colour = (r, g, b)
    else:
        response.set_status(400, "Unable to connect to device")

    return response.to_json()
    
@app.route("/register")
def register_device():
    response = APIResponse()

    mac = request.args.get("mac")
    name = request.args.get("name")

    if mac == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if name == None:
        response.set_status(400, "Missing device name")
        return response.to_json()

    register_device(mac, name)
    response.set_status(200, "Registered device")
    return response.to_json()

@app.route("/raw")
def raw_packet():
    response = APIResponse()

    if not config["dev_mode"]:
        response.set_status(403, "Development mode is disabled")
        return response.to_json()

    device = request.args.get("device")
    packet = request.args.get("packet")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if packet == None:
        response.set_status(400, "Missing packet data")
        return response.to_json()

    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        #No update to the device settings via raw packet entries
    else:
        response.set_status(400, "Error sending raw packet")

    return response.to_json()
