from flask import request, Flask
import json

app = Flask(__name__)

@app.route("/status")
def status():
    print("status")

@app.route("/order")
def order():
    print("order")
