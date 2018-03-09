from core import *

dev = find_device([(0xfce, 0x518c)])
#toggle_accessory_mode(dev, "PedalPi", "Display-View", "Description", "1.0", "http://www.github.com/PedalPi/DisplayView", "SN-123-456-789")
#toggle_accessory_mode(dev, "Manufacturer", "Model", "Description", "1.0", "http://www.github.com/PedalPi/DisplayView", "SN-123-456-789")

MANUFACTURER = "Pedal Pi"
MODEL_NAME = "Display View"
DESCRIPTION = "Pedal Pi - Display View"
VERSION = "0.3.0"
URL = "http://github.com/PedalPi/DisplayView"
SERIAL_NUMBER = "0001"

toggle_accessory_mode(dev, MANUFACTURER, MODEL_NAME, DESCRIPTION, VERSION, URL, SERIAL_NUMBER)
dev = find_accessory()

import time
time.sleep(100)