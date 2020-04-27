class GoveePacket:
    def __init__(self, identifier):
        self.identifier = identifier
        self.data = 0
        self.sig = identifier

    def set_data_byte(self, pos, intv):
        if intv < 0 or intv > 255:
            return

        self.sig = self.sig ^ intv
        pos_val = intv << ((17 - pos) * 8)
        #clear_mask = (2 ** 8) ** 20 - 1
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
        structure.set_data([5, 2, r, g, b, 0])
        return structure.generate()

    @staticmethod
    def temperature_packet(kelvin):
        structure = GoveePacket(51)
        trgb = calculate_kelvin_rgb(kelvin)
        structure.set_data([5, 2, 255, 255, 255, 1, trgb["r"], trgb["g"], trgb["b"]])
        return structure.generate()

    @staticmethod
    def hsb_packet(hue, saturation, brightness):
        pass

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

    @staticmethod
    def on_packet():
        structure = GoveePacket(51)
        structure.set_data([1, 1])
        return structure.generate()

    @staticmethod
    def off_packet():
        structure = GoveePacket(51)
        structure.set_data([1])
        return structure.generate()

    @staticmethod
    def music_mode_packet(sensitivity, r, g, b):
        structure = GoveePacket(51)
        structure.set_data([5, 3, 1, sensitivity, r, g, b])
        return structure.generate()

def fix_hex_length(intv, length):
    h = hex(intv).replace("0x", "")
    h = (length * 2 - len(h)) * "0" + h
    return h

#Algorithm from https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
def calculate_kelvin_rgb(kelvin):
    if kelvin <= 1000:
        kelvin = 1001
    elif kelvin >= 6600:
        kelvin = 6599

    temperature = kelvin / 100
    r, g, b = 0, 0, 0

    #Calculate red
    if temperature <= 66:
        r = 255
    else:
        r = temperature - 60
        r = 329.698727446 * pow(r, -0.1332047592)

    if r < 0:
        r = 0
    elif r > 255:
        r = 255

    #Calculate green
    if temperature <= 66:
        g = temperature
        g = 99.4708025861 * math.log(g) - 161.1195681661
    else:
        g = temperature - 60
        g = 288.1221695283 * pow(g, -0.0755148492)

    if g < 0:
        g = 0
    elif g > 255:
        g = 255

    #Calculate blue
    if temperature >= 66:
        b = 0
    else:
        b = temperature - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307

    if b < 0:
        b = 0
    elif b > 255:
        b = 255

    return {
        "r": int(r),
        "g": int(g),
        "b": int(b)
    }
