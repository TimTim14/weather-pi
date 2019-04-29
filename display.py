#!/usr/bin/env python3
import os
import requests
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
API_ENDPOINT = "http://clelland.shelms.io/api/"

def report():
    data = bme280.sample(bus, address, calibration_params)
    t = {'celsius': data.temperature}
    r = requests.post(API_ENDPOINT , t)
    h = requests.post(API_ENDPOINT + 'rh/',
    data ={'rh': data.humidity})
    p = requests.post(API_ENDPOINT + 'bh/',
    data ={'bp': data.pressure})
    print(r.text)
    print(h.text)
    print(p.text)
def main():
    time_counter = 0

    # define our i2c LED location
    serial = i2c(port=1, address=0x3C)

    # We have an ssd1306 device so we initialize it at the 
    # serial address we created.
    oled_device = ssd1306(serial)

    # This line keeps the display from immediately turning off once the
    # script is complete.
    oled_device.cleanup = do_nothing


	  # Update our LED
    #stats(oled_device)

	  # Every 5 minutes post up to our production site.
	  # Feel free to change this or eliminate this during testing.
    if (time_counter % 10 == 0):
            report()

	  # Increment a counter (1 per second. 5 here since we sleep 5 below)
    time_counter += 5

	  # Sleep 5 second
    data = bme280.sample(bus, address, calibration_params)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30,5), "temperature", fill="white")
        draw.text((15,15), str(data.temperature * (9/5) + 32), fill="white") 
        draw.text((35,30), "date/time", fill="white")
        draw.text((2,40), str(data.timestamp), fill="white")

        print(data.temperature * (9/5) + 32)
        print(data.humidity)
        print(data.pressure)
while True:
    main()
    time.sleep(2)
