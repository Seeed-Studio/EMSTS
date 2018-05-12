from evdev import InputDevice,categorize,ecodes
from pixel_ring import pixel_ring
import mraa
import os
import time

time.sleep(5)
key = InputDevice("/dev/input/event0")
en = mraa.Gpio(12)
if os.geteuid() != 0 :
    time.sleep(1)

en.dir(mraa.DIR_OUT)
en.write(0)
leds = pixel_ring.dev
for event in key.read_loop():
    if event.type == ecodes.EV_KEY:
        if categorize(event).keystate == 2:
            for ii in range(12):
                leds.set_pixel(ii, 125, 125, 125)   
                leds.show() 

