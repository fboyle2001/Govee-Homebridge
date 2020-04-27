from flask import request, Flask
from request_receiver_util import *
from config import config
import device_handler
import packets

app = Flask(__name__)

@app.route("/api/update/on")
def turn_light_on():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        response.set_status(400, "Missing mac address")
        return response.display()

    packet = packets.GoveePacket.on_packet()
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_light_on_callback, None)
    response.set_status(200)

    return response.display()

def update_light_on_callback(device, value):
    device.on = True

@app.route("/api/update/off")
def turn_light_off():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        response.set_status(400, "Missing mac address")
        return response.display()

    packet = packets.GoveePacket.off_packet()
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_light_off_callback, None)
    response.set_status(200)

    return response.display()

def update_light_off_callback(device, value):
    device.on = False

@app.route("/api/update/brightness")
def update_brightness():
    response = APIResponse()
    mac = request.args.get("mac")
    brightness = request.args.get("brightness")

    if mac == None:
        response.set_status(400, "Missing mac address")
        return response.display()

    if brightness == None:
        response.set_status(400, "Missing brightness")
        return response.display()
    else:
        brightness = validate_integer(response, "brightness", brightness, 0, 255)
        if brightness == None:
            return response.display()

    packet = packets.GoveePacket.brightness_packet(brightness)
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_brightness_callback, brightness)
    response.set_status(200)

    return response.display()

def update_brightness_callback(device, value):
    device.brightness = value

@app.route("/api/read/brightness")
def get_brightness():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        response.set_status(400, "Missing mac address")
        return response.display()

    device = device_handler.get_device(mac)
    response.set_status(200)
    response.set_data("brightness", device.brightness)

    return response.display()
