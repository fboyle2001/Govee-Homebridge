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
