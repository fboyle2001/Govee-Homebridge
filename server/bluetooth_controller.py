import pexpect

class GoveePacket:
    def __init__(self, identifier):
        self.identifier = identifier
        self.data = 0
        self.sig = identifier

    def set_data_byte(self, pos, intv):
        assert 0 <= intv <= 255
        self.sig = self.sig ^ intv
        pos_val = intv << ((17 - pos) * 8)
        clear_mask = (2 ** 8) ** 20 - 1
        #need a way to wipe a byte, use an AND with 111..1000000001..111
        self.data = self.data | pos_val

    def set_data(self, data):
        for index, byte in enumerate(data):
            self.set_data_byte(index, byte)

    def generate(self):
        sgm_id = fix_hex_length(self.identifier, 1)
        sgm_data = fix_hex_length(self.data, 18)
        sgm_xor = fix_hex_length(self.sig, 1)
        return sgm_id + sgm_data + sgm_xor

    @staticmethod
    def rgb_packet(r, g, b):
        structure = GoveePacket(51)
        structure.set_data([5, 2, r, g, b, 0, 255, 174, 84])
        return structure.generate()

    @staticmethod
    def brightness_packet(level):
        structure = GoveePacket(51)
        structure.set_data([4, level])
        return structure.generate()

    @staticmethod
    def keep_alive_packet():
        structure = GoveePacket(170)
        structure.set_data([1])
        return structure.generate()

def fix_hex_length(intv, length):
    h = hex(intv).replace("0x", "")
    h = (length * 2 - len(h)) * "0" + h
    return h

def send_command(gatt, device, packet):
    gatt.sendline(f"connect {device}")

    try:
        gatt.expect("Connection successful", timeout=5)
    except pexpect.exceptions.TIMEOUT:
        return False

    gatt.sendline(f"char-write-cmd 0x0015 {packet}")
    gatt.expect(".*")
    gatt.sendline("disconnect")
    gatt.expect(".*")

    return True
