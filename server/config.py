config = {
    "dev_mode": True,
    "linux": False
}

import os.path

if os.path.isfile("linux_mode.config"):
    print("Using Linux mode")
    config["linux"] = True
else:
    print("Using Windows mode")
