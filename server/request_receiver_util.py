import json

class APIResponse:
    default_messages = {
        200: "Success",
        400: "Bad Request",
        403: "Forbidden",
        500: "Internal Server Error"
    }

    def __init__(self, code = None, message = None):
        if code == None:
            self.status = dict()
        else:
            self.set_status(code, message)

        self.data = dict()

    def set_status(self, code, message = None):
        self.status = {
            "code": code,
            "message": self.default_messages[code] if message == None else message
        }

    def set_data(self, key, value):
        self.data[key] = value

    def display(self):
        return json.dumps(self, default = lambda k: k.__dict__, sort_keys = True, indent = 2), self.status["code"]

def validate_integer(response, name, value, min, max):
    int_val = value

    try:
        int_val = int(int_val)
    except ValueError:
        response.set_status(400, f"{name} must be an integer between {min} and {max}")
        return None

    if int_val < min:
        int_val = min
    elif int_val > max:
        int_val = max

    return int_val

#https://gist.github.com/mjackson/5311256
def hsl_to_rgb_helper(p, q, t):
    if t < 0:
        t += 1
    elif t > 1:
        t -= 1

    if t < 1/6:
        return p + (q - p) * 6 * t
    elif t < 1/2:
        return q
    elif t < 2/3:
        return p + (q - p) * (2/3 - t) * 6

    return p

#https://gist.github.com/mjackson/5311256
def hsl_to_rgb(h, s, l):
    if s == 0:
        return 0, 0, 0

    q = l + s - l * s

    if l < 0.5:
        q = l * (1 + s)

    p = 2 * l - q

    print(p, q)

    r = hsl_to_rgb_helper(p, q, h + 1/3) * 255
    g = hsl_to_rgb_helper(p, q, h) * 255
    b = hsl_to_rgb_helper(p, q, h - 1/3) * 255

    return int(r), int(g), int(b)
