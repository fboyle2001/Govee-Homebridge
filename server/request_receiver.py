from flask import request, Flask
import device_handler
from request_receiver_util import *
from config import config
import packets

app = Flask(__name__)

@app.route("/api/on")
def turn_light_on():
    response = APIResponse()
    mac = request.args.get("mac")

    if mac == None:
        response.set_status(400, "Missing mac address")
        return response.to_json()

    packet = packets.GoveePacket.on_packet()
    device = device_handler.get_device(mac)
    device.packet_processor.queue_packet(packet, lambda device: device.on = True)
    response.set_status(200)

    return response.to_json()
