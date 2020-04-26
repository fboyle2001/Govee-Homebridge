from flask import request, Flask
import bluetooth_controller as controller
from api_routes_util import *

app = Flask(__name__)

@app.route("/error_generate/500")
def test_r():
    response = APIResponse()
    response.set_status(500)
    return response.to_json()

@app.route("/get_brightness")
def get_brightness():
    response = APIResponse()
    device = request.args.get("device")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    current = get_device(device).brightness

    response.add_data("brightness", current)
    response.set_status(200)
    return response.to_json()

@app.route("/status")
def get_device_status():
    response = APIResponse()
    device = request.args.get("device")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    current = get_device(device).on

    response.add_data("status", current)
    response.set_status(200)
    return response.to_json()

@app.route("/toggle")
def toggle_light():
    response = APIResponse()
    device = request.args.get("device")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    current = get_device(device).on
    packet = controller.GoveePacket.on_packet()

    if current:
        packet = controller.GoveePacket.off_packet()

    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).on = not current
    else:
        response.set_status(500, "Unable to connect to device")

    return response.to_json()

@app.route("/on")
def turn_light_on():
    response = APIResponse()
    device = request.args.get("device")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    packet = controller.GoveePacket.on_packet()
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).on = True
    else:
        response.set_status(500, "Unable to connect to device")

    return response.to_json()

@app.route("/off")
def turn_light_off():
    response = APIResponse()
    device = request.args.get("device")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    packet = controller.GoveePacket.off_packet()
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).on = False
    else:
        response.set_status(500, "Unable to connect to device")

    return response.to_json()

@app.route("/music")
def music_mode():
    response = APIResponse()
    device = request.args.get("device")
    sens = request.args.get("sens")
    r = request.args.get("r")
    g = request.args.get("g")
    b = request.args.get("b")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if sens == None:
        sens = 128
    else:
        sens = validate_integer(response, "sens", sens, 0, 255)
        if sens == None:
            return response.to_json()

    if r == None:
        r = 0
    else:
        r = validate_integer(response, "r", r, 0, 255)
        if r == None:
            return response.to_json()

    if g == None:
        g = 0
    else:
        g = validate_integer(response, "g", g, 0, 255)
        if g == None:
            return response.to_json()

    if b == None:
        b = 0
    else:
        b = validate_integer(response, "b", b, 0, 255)
        if b == None:
            return response.to_json()

    packet = controller.GoveePacket.music_mode_packet(sens, r, g, b)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).sensitivity = sens
        get_device(device).mode = 2
        get_device(device).colour = (r, g, b)
    else:
        response.set_status(500, "Unable to connect to device")

    return response.to_json()

@app.route("/temperature")
def change_temperature():
    response = APIResponse()
    device = request.args.get("device")
    temperature = request.args.get("temperature")

    if device == None:
        response.set_status(400, "Missing device address")
        return response.to_json()

    if temperature == None:
        response.set_status(400, "Missing temperature")
        return response.to_json()
    else:
        temperature = validate_integer(response, "temperature", temperature, 1001, 6599)
        if temperature == None:
            return response.to_json()

    packet = controller.GoveePacket.temperature_packet(temperature)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).temperature = temperature
        get_device(device).mode = 1
    else:
        response.set_status(500, "Unable to connect to device")

    return response.to_json()

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
        level = validate_integer(response, "level", level, 0, 255)
        if level == None:
            return response.to_json()

    packet = controller.GoveePacket.brightness_packet(level)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).brightness = level
    else:
        response.set_status(500, "Unable to connect to device")

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
        r = validate_integer(response, "r", r, 0, 255)
        if r == None:
            return response.to_json()

    if g == None:
        g = 0
    else:
        g = validate_integer(response, "g", g, 0, 255)
        if g == None:
            return response.to_json()

    if b == None:
        b = 0
    else:
        b = validate_integer(response, "b", b, 0, 255)
        if b == None:
            return response.to_json()

    packet = controller.GoveePacket.rgb_packet(r, g, b)
    success = controller.send_command(gatt, device, packet)

    if success == True:
        response.set_status(200)
        get_device(device).colour = (r, g, b)
        get_device(device).mode = 0
    else:
        response.set_status(500, "Unable to connect to device")

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

    register_led_device(mac, name)
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
        response.set_status(500, "Error sending raw packet")

    return response.to_json()
