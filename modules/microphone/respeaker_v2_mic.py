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
from kernel import core
import time
import os
from lib import recorder
import numpy as np
import audioop
from evdev import InputDevice,categorize,ecodes


class subcore(core.interface):
    def __init__(self,parameters,platform,debug):
        super(subcore,self).__init__(parameters)
        self.parameters = parameters
        self.platform = platform
        self.debug  = debug
        self.ret = {
            "description": self.parameters["description"],
            "result": "watch"
        }
        self.key = InputDevice("/dev/input/event0")
    def do_test(self):
        counter = 0
        self.debug("show")
        led_status = ["1","1","1","1","1","1","1","1","1","1","1","1"]
        led_location = [10,0,2,4,6,8]
        mic_rms = [0,0,0,0,0,0]
        for event in self.key.read_loop():
            if event.type == ecodes.EV_KEY:
                if categorize(event).keystate == 2:
                    time.sleep(4)
                    if self.platform == "respeaker v2":
                        os.system("arecord -d 1 -f S16_LE -r 16000 -Dhw:0,0 -c 8 /tmp/aaa.wav")
                    with recorder.recorder(16000, 8, 16000 / 16)  as mic:
                        for chunk in mic.read_chunks():
                            for i in range(6):
                                data = np.fromstring(chunk, dtype='int16')
                                data = data[i::8].tostring()
                                rms = audioop.rms(data, 2)
                                #rms_db = 20 * np.log10(rms)
                                #print('channel: {} RMS: {} dB'.format(i,rms))
                                if counter != 0:
                                    mic_rms[i] = mic_rms[i] + rms
                                                           
                            if counter == 10:
                                break
                            counter = counter + 1 

                    break
        for i in range(6):
            mic_rms[i] = mic_rms[i] / 10
            print('channel: {} RMS: {} dB'.format(i,mic_rms[i]))
            if self.parameters["value"] - self.parameters["bias"] > mic_rms[i]  \
            or self.parameters["value"] + self.parameters["bias"] < mic_rms[i]:
                led_status[led_location[i]] = "0"
        self.debug("".join(led_status))
        return self.ret

