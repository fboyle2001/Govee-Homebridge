config = {
    "dev_mode": True,
    "linux": False
}

try:
    f = open("linux_mode.config")
    config["linux"] = True
    print("Using Linux mode")
except FileNotFoundError:
    pass
