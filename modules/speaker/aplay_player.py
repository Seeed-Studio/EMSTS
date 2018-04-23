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
import threading
from lib import recorder
import numpy as np
import audioop
import pyaudio
import wave


def play_music(p):
    os.popen(" aplay -D " +p["device"] +" /opt/music/"+p["music"])


class subcore(core.interface):
    def __init__(self,parameters,platform,debug):
        super(subcore,self).__init__(parameters)
        self.parameters = parameters
        self.platform = platform
        self.debug  = debug
        self.ret = {
            "description": self.parameters["description"],
            "result": "ok"
        }
    def do_test(self):
        if self.platform == "respeaker v2":
            os.system("arecord -d 1 -f S16_LE -r 16000 -Dhw:0,0 -c 8 /tmp/aaa.wav")
        t =threading.Thread(target=play_music,args=(self.parameters,))
        t.start()
        counter = 0
        mic_rms = [0,0,0,0,0,0,0,0]
        all_rms = 0
        rms = 0
        RATE = 16000
        CHUNK = 2048
        RECORD_SECONDS = 5
        if self.platform == "respeaker v2":
            time.sleep(3)

            os.system("arecord -d 7 -f S16_LE -r 16000 -Dhw:0,0 -c 8 /tmp/bbb.wav")
            
            wf = wave.open("/tmp/bbb.wav","rb")

            chunk = wf.readframes(CHUNK)
            while chunk != b'':
                for ii in range(8):
                    data = np.fromstring(chunk, dtype='int16')
                    data = data[ii::8].tostring()
                    rms = audioop.rms(data, 2)
                    #rms_db = 20 * np.log10(rms)
                    #print('channel: {} RMS: {} dB'.format(ii,rms_db))
                    if counter > 19:
                        mic_rms[ii] = mic_rms[ii] + rms                        
                                                             
                if counter == 50:
                    break
                counter = counter + 1   
                chunk = wf.readframes(CHUNK)
        for i in range(8):
            mic_rms[i] = mic_rms[i] / 30
            print('channel: {} RMS: {}'.format(i,mic_rms[i]))                           
            if i == 6:
                if self.parameters["ch7"] - self.parameters["bias_c"] > mic_rms[i]  \
                or self.parameters["ch7"] + self.parameters["bias_c"] < mic_rms[i]:
                    self.ret["result"] = "ch7"  
                    break
            if i == 7:
                if self.parameters["ch8"] - self.parameters["bias_c"] > mic_rms[i]  \
                or self.parameters["ch8"] + self.parameters["bias_c"] < mic_rms[i]:
                    self.ret["result"] = "ch8"
                    break

            if i != 6 and i != 7:
                if mic_rms[i] < self.parameters["mini"] :
                    self.ret["result"] = str(i)
                    break                
        return self.ret
