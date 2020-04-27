from queue import Queue
from config import config
import threading
import packets
import pexpect
import time

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

        self.packet_processor.start_processing()

class DevicePacketProcessor:
    def __init__(self, device):
        self.device = device
        self.waiting_packets = Queue()
        self.active = False
        self.processing_thread = None
        self.send_alive_packet_period = 0.2
        self.delay_packet_period = 0.05
        self.max_connect_attempts = 5

    def queue_packet(self, packet, callback, value):
        self.waiting_packets.put((packet, callback, value))

    def stop_processing(self):
        self.active = False

    def start_processing(self):
        self.processing_thread = threading.Thread(target=self.process_packets)
        self.processing_thread.setDaemon(True)
        self.processing_thread.start()

    def process_packets(self):
        self.active = True
        gatt_instance = PExpectMock()
        if config["linux"]:
            gatt_instance = pexpect.spawn("gatttool -I")
        connected = False

        for i in range(self.max_connect_attempts):
            gatt_instance.sendline(f"connect {self.device.mac}")

            try:
                gatt_instance.expect("Connection successful", timeout = 3)
                connected = True
                break
            except pexpect.exceptions.TIMEOUT:
                pass

        if not connected:
            raise ConnectionError("Unable to connect to " + self.device.mac)

        while self.active:
            while self.waiting_packets.qsize() != 0:
                packet, callback, value = self.waiting_packets.get()
                gatt_instance.sendline(f"char-write-cmd 0x0015 {packet}")
                gatt_instance.expect(".*")
                self.waiting_packets.task_done()
                if callback != None:
                    callback(self.device, value)
                time.sleep(self.delay_packet_period)

            gatt_instance.sendline(packets.GoveePacket.keep_alive_packet())
            gatt_instance.expect(".*")

            time.sleep(self.send_alive_packet_period)

        gatt_instance.sendline("disconnect")
        gatt_instance.expect(".*")

DEVICE_REGISTER = {}

def get_device(mac):
    if mac not in DEVICE_REGISTER:
        DEVICE_REGISTER[mac] = Device(mac)

    return DEVICE_REGISTER[mac]
