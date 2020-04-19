config = {
    "dev_mode": True,
    "linux": False
}

try:
    f = open("linux_mode.config")
    config["linux"] = True
except IOError:
    pass
finally:
    f.close()
