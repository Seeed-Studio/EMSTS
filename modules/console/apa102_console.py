#!/usr/bin/env python
# Author: Baozhu Zuo <zuobaozhu@gmail.com>
# Copyright (c) 2018 Seeed Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



from pixel_ring import pixel_ring
import mraa
import time
import os

class console:
    def __init__(self,parameters,platform):
        en = mraa.Gpio(12)
        if os.geteuid() != 0 :
            time.sleep(1)
        
        en.dir(mraa.DIR_OUT)
        en.write(0)

        self.leds = pixel_ring.dev

    def log(self,*args):
        for a in args:
            print(a)

    def debug(self,*args):
        for a in args:
            print(a)
            if a == "show":
                for ii in range(12):
                    self.leds.set_pixel(ii, 255, 255, 255)   
                    self.leds.show() 
                return 
            counter = 0
            for ii in a:
                if ii == "1":
                    self.leds.set_pixel(counter, 0, 0, 255)
                else:
                    self.leds.set_pixel(counter, 255, 0, 0)   
                self.leds.show()  
                counter = counter + 1