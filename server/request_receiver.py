from flask import request, Flask
from request_receiver_util import *
from config import config
import device_handler
import packets
import logging

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
console_handler.setFormatter(console_format)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s %(name)s:%(funcName)20s():%(lineno)s [%(levelname)s] - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

@app.route("/api/update/hs")
def hue_saturation_update():
    response = APIResponse()
    mac = request.args.get("mac")
    hue = request.args.get("hue")
    saturation = request.args.get("saturation")

    if mac == None:
        logger.warning("Rejected request to change colour: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    if hue == None:
        logger.warning("Rejected request to change colour: missing hue")
        response.set_status(400, "Missing hue")
        return response.display()
    else:
        hue = validate_integer(response, "hue", hue, 0, 360)
        if hue == None:
            return response.display()

    if saturation == None:
        logger.warning("Rejected request to change colour: missing saturation")
        response.set_status(400, "Missing saturation")
        return response.display()
    else:
        saturation = validate_integer(response, "saturation", saturation, 0, 100)
        if saturation == None:
            return response.display()

    device = device_handler.get_device(mac)
    brightness = device.brightness
    r, g, b = hsl_to_rgb(hue / 360, saturation / 100, brightness / 100)
    packet = packets.GoveePacket.rgb_packet(r, g, b)
    device.packet_processor.queue_packet(packet, update_colour_callback, (r, g, b))
    response.set_status(200)
    logger.info(f"Queued colour packet for {mac} and sending 200 response")

    return response.display()

def update_colour_callback(device, colour):
    device.colour = colour
    logger.info(f"Colour packet sent to {device.mac}. Callback called, updated colour value to {colour}")

@app.route("/api/update/on")
def turn_light_on():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        logger.warning("Rejected request to turn light on: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    packet = packets.GoveePacket.on_packet()
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_light_on_callback, None)
    response.set_status(200)
    logger.info(f"Queued on packet for {mac} and sending 200 response")

    return response.display()

def update_light_on_callback(device, value):
    device.on = True
    logger.info(f"On packet sent to {device.mac}. Callback called, updated on value to True")

@app.route("/api/update/off")
def turn_light_off():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        logger.warning("Rejected request to turn light off: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    packet = packets.GoveePacket.off_packet()
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_light_off_callback, None)
    response.set_status(200)
    logger.info(f"Queued off packet for {mac} and sending 200 response")

    return response.display()

def update_light_off_callback(device, value):
    device.on = False
    logger.info(f"Off packet sent to {device.mac}. Callback called, updated on value to False")

@app.route("/api/update/brightness")
def update_brightness():
    response = APIResponse()
    mac = request.args.get("mac")
    brightness = request.args.get("brightness")

    if mac == None:
        logger.warning("Rejected request to update brightness: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    if brightness == None:
        logger.warning("Rejected request to update brightness: missing brightness level")
        response.set_status(400, "Missing brightness")
        return response.display()
    else:
        brightness = validate_integer(response, "brightness", brightness, 0, 100)
        if brightness == None:
            return response.display()

    packet = packets.GoveePacket.brightness_packet(brightness)
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, update_brightness_callback, brightness)
    response.set_status(200)
    logger.info(f"Queued brightness packet for {mac} with brightness level {brightness} and sending 200 response")

    return response.display()

def update_brightness_callback(device, brightness):
    device.brightness = brightness
    device.on = True
    logger.info(f"Brightness packet sent to {device.mac}. Callback called, updated brightness value to {brightness}")

@app.route("/api/read/brightness")
def get_brightness():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        logger.warning("Rejected request to read brightness: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    device = device_handler.get_device(mac)
    response.set_status(200)
    response.set_data("brightness", device.brightness)
    logger.info(f"Read brightness for {mac}, sending 200 response")

    return response.display()

@app.route("/api/read/status")
def get_light_status():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        logger.warning("Rejected request to read status: missing MAC address")
        response.set_status(400, "Missing MAC address")
        return response.display()

    device = device_handler.get_device(mac)
    response.set_status(200)
    response.set_data("status", device.on)
    logger.info(f"Read status for {mac}, sending 200 response")

    return response.display()
