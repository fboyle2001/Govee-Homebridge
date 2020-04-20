from flask import request, Flask
import json

app = Flask(__name__)
class State:
    def __init__(self):
        self.currentState = True

    def toggle(self):
        self.currentState = not self.currentState

    def to_json(self):
        return json.dumps(self, default = lambda k: k.__dict__, sort_keys = True, indent = 2)

s = State()

@app.route("/api/status")
def status():
    print("status")
    print(s.to_json())
    return s.to_json()

@app.route("/api/order")
def order():
    print("order")
    print(s.to_json())
    s.toggle()
    return s.to_json()
