config = {
    "dev_mode": True,
    "linux": False
}

import os.path

linux_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "linux_mode.config")

if os.path.isfile(linux_path):
    print("Using Linux mode")
    config["linux"] = True
else:
    print("Using Windows mode")
