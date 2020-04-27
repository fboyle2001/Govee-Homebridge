import threading
from queue import Queue
import packets

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

    def queue_packet(self, packet, callback):
        self.waiting_packets.put((packet, callback))

    def stop_processing(self):
        self.active = False

    def start_processing(self):
        self.processing_thread = threading.Thread(target=self.process_packets)

    def process_packets(self):
        self.active = True
        gatt_instance = pexpect.spawn("gatttool -I")
        connected = False

        for i in range(self.max_connect_attempts):
            gatt.sendline(f"connect {self.device.mac}")

            try:
                gatt.expect("Connection successful", timeout = 3)
                connected = True
                break
            except pexpect.exceptions.TIMEOUT:
                pass

        if not connected:
            raise ConnectionError("Unable to connect to " + self.device.mac)

        while self.active:
            for packet, callback in self.waiting_packets:
                gatt_instance.sendline(f"char-write-cmd 0x0015 {packet}")
                gatt_instance.expect(".*")
                self.waiting_packets.task_done()
                callback(self.device)
                sleep(self.delay_packet_period)

            gatt_instance.sendline(packets.GoveePacket.keep_alive_packet())
            gatt_instance.expect(".*")

            sleep(self.send_alive_packet_period)

        gatt_instance.sendline("disconnect")
        gatt_instance.expect(".*")

DEVICE_REGISTER = {
    "mac": Device("mac")
}#

def get_device(mac):
    pass
