from queue import Queue
from config import config
import threading
import packets
import pexpect
import time
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] - %(message)s')
console_handler.setFormatter(console_format)

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)
file_format = logging.Formatter('%(asctime)s %(name)s:%(funcName)20s():%(lineno)s [%(levelname)s] - %(message)s')
file_handler.setFormatter(file_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

class PExpectMock:
    def sendline(self, data):
        return True

    def expect(self, data, timeout=100):
        return True

class Device:
    def __init__(self, mac):
        self.mac = mac

        self.packet_processor = DevicePacketProcessor(self)
        self.on = False
        self.brightness = 0
        self.colour = (0, 0, 0)

class DevicePacketProcessor:
    def __init__(self, device):
        self.device = device
        self.waiting_packets = Queue()
        self.active = False
        self.processing_thread = None

        self.send_alive_packet_period = 1.0
        self.delay_packet_period =      1.0

        self.max_total_loops =          6
        self.max_empty_loops =          2
        self.max_connect_attempts =     5

    def queue_packet(self, packet, callback, value):
        self.waiting_packets.put((packet, callback, value))
        logger.debug(f"Queued {packet} on {self.device.mac}, using callback {callback} with arg {value}")

        if self.active == False:
            self.start_processing()

    def stop_processing(self):
        self.active = False
        logger.info(f"Stopped packet processing for {self.device.mac}")

    def start_processing(self):
        self.processing_thread = threading.Thread(target=self.process_packets)
        self.processing_thread.setDaemon(True)
        self.processing_thread.start()
        logger.info(f"Started packet processing for {self.device.mac}")

    def process_packets(self):
        self.active = True
        gatt_instance = PExpectMock()

        if config["linux"]:
            logger.debug(f"Using Linux configuration so using gatttool")
            gatt_instance = pexpect.spawn("gatttool -I")
            gatt_instance.logfile = sys.stdout.buffer
        else:
            logger.debug(f"Using Windows configuration so using PExpectMock")


        connected = False

        for i in range(self.max_connect_attempts):
            gatt_instance.sendline(f"connect {self.device.mac}")

            try:
                gatt_instance.expect("Connection successful", timeout = 3)
                connected = True
                break
            except pexpect.exceptions.TIMEOUT:
                attempt = i + 1
                logger.warning(f"Failed to connect to {self.device.mac}, attempt {attempt}/{self.max_connect_attempts}")

        if not connected:
            logger.critical(f"Unable to connect to {self.device.mac}")
            raise ConnectionError("Unable to connect to " + self.device.mac)

        empty_loops = 0
        total_loops = 0

        while self.active:
            sent_packets = 0

            if self.waiting_packets.qsize() == 0:
                empty_loops += 1

            while self.waiting_packets.qsize() != 0:
                empty_loops = 0
                if sent_packets >= 16:
                    break

                packet, callback, value = self.waiting_packets.get()
                logger.debug(f"Found {packet} to send to {self.device.mac}")
                sent_bytes = gatt_instance.sendline(f"char-write-cmd 0x0015 {packet}")
                logger.debug(f"Sent {sent_bytes} in {packet} to {self.device.mac}")
                k = gatt_instance.expect(".*")
                self.waiting_packets.task_done()
                logger.debug(f"Sent {packet} to {self.device.mac}")
                if callback != None:
                    callback(self.device, value)
                sent_packets += 1
                time.sleep(self.delay_packet_period)

            logger.debug(f"Depleted waiting packet queue for {self.device.mac}")

            if total_loops == self.max_total_loops or empty_loops == self.max_empty_loops:
                logger.info(f"Reached {total_loops} total loops and {empty_loops} empty loops")
                break

            gatt_instance.sendline(packets.GoveePacket.keep_alive_packet())
            k = gatt_instance.expect(".*")
            logger.debug(f"KEEP ALIVE {k}")
            logger.debug(f"Last response: {gatt_instance.before}")

            logger.debug(f"Sent keep alive packet to {self.device.mac}")
            total_loops += 1
            time.sleep(self.send_alive_packet_period)

        gatt_instance.sendline("disconnect")
        gatt_instance.expect(".*")
        logger.info(f"Disconnected from {self.device.mac}")
        self.active = False

DEVICE_REGISTER = {}

def get_device(mac):
    if mac not in DEVICE_REGISTER:
        DEVICE_REGISTER[mac] = Device(mac)
        logger.info(f"Registered new device with mac address {mac}")

    return DEVICE_REGISTER[mac]
