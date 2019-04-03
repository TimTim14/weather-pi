#!/usr/bin/env python3
import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

import smbus2
import bme280

def do_nothing(obj):
    pass

from PIL import ImageFont
import time

# define our i2c LED location
serial = i2c(port=1, address=0x3C)
# We have an ssd1306 device so we initialize it at the
# serial address we created.
device = ssd1306(serial)
# This line keeps the display from immediately turning off once the
# script is complete.
device.cleanup = do_nothing

# Setup our Temperature sensor (bme280)
port = 4
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)



def main():
    data = bme280.sample(bus, address, calibration_params)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30,5), "temperature", fill="white")
        draw.text((15,15), str(data.temperature * (9/5) + 32), fill="white") 
        draw.text((35,30), "date/time", fill="white")
        draw.text((2,40), str(data.timestamp), fill="white")
        
        
        print(data.temperature * (9/5) + 32)
        print(data.humidity)
        
while True:   
    main()
    time.sleep(2)     