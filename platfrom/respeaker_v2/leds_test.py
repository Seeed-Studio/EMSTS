import time
from evdev import InputDevice,categorize,ecodes
from pixel_ring.apa102_pixel_ring import PixelRing
import mraa
import os

pixel_ring = PixelRing()

key = InputDevice("/dev/input/event0")
en = mraa.Gpio(12)

while os.geteuid() != 0 :
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


