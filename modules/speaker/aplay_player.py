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
from lib.snowboy import snowboydecoder
import numpy as np
import audioop
from dtw import dtw
from numpy.linalg import norm
from python_speech_features import mfcc
from python_speech_features import logfbank
import wave

def play_white(p):
    os.popen(" aplay -D " +p["device"] +" /opt/music/white.wav")

def play_music(p):
    os.popen(" aplay -D " +p["device"] +" /opt/music/"+p["music"])

def mic_array_arecord(p):
    os.popen("arecord -D hw:seeed8micvoicec -r 16000 -c 8 -f  S16_LE -d 2 /tmp/mic_array.wav")

def usb_audio_arecord(p):
    os.popen("arecord -D hw:ArrayUAC10 -r 16000 -c 6 -f  S16_LE -d 2 /tmp/usb_audio.wav ")

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
            sensitivity = 0.5
            CHUNK=1024+256
            mic_rms = [0,0,0,0,0,0,0,0]
            counter = 0
            min_rms_counter = 0
            avg_min_rms = 0


            os.system("arecord -d 1 -f S16_LE -r 16000 -Dhw:0,0 -c 8 /tmp/aaa.wav")
            

            play_thread =threading.Thread(target=play_music,args=(self.parameters,))
            play_thread.start()

            mic_array_thread =threading.Thread(target=mic_array_arecord,args=(self.parameters,))
            mic_array_thread.start()

            usb_audio_thread =threading.Thread(target=usb_audio_arecord,args=(self.parameters,))
            usb_audio_thread.start()


            time.sleep(3)
            #1, 先用参考麦克风用snowboy先对环境进行测试如果不合适，重新录音
            usb_audio_wave = wave.open("/tmp/usb_audio.wav","rb")
            
            chunk1 = usb_audio_wave.readframes(usb_audio_wave.getnframes())        
            data1 = np.fromstring(chunk1, dtype='int16')
            detection = snowboydecoder.HotwordDetector("/home/respeaker/respeaker_v2_f/lib/snowboy/resources/models/snowboy.umdl", sensitivity=sensitivity)
            ans = detection.detector.RunDetection(np.array(data1[4::6], dtype=np.int16).tobytes())
            if ans == 1:
                print('Hotword Detected!')
            else:
                print('usb not hotword Detected!')
                #播放警告信息
                os.popen(" aplay -D " +self.parameters["device"] +" /opt/music/warning1.wav")
                self.ret["result"] = "failed"
                return self.ret

            usb_audio_wave.close()

            #重新打开usb_audio的wav文件，检测当前环境是否安静
            usb_mic_array_rms = wave.open("/tmp/usb_audio.wav","rb")
            chunk = usb_mic_array_rms.readframes(CHUNK)
            usb_min_rms_counter = 0
            usb_avg_val = 0  
            while chunk != b'':       
                data = np.fromstring(chunk, dtype='int16')
                data = data[4::8].tostring()
                rms = audioop.rms(data, 2)

                        
                #rms是对静噪的测试，所以只考虑麦克风能量值平均值在600以内的窗
                if rms < 350:
                    usb_avg_val = usb_avg_val + rms
                    usb_min_rms_counter += 1

                chunk = usb_mic_array_rms.readframes(CHUNK)
            print("usb min rms counter:",usb_min_rms_counter)
            if usb_min_rms_counter < 10:
                #播放警告信息
                os.popen(" aplay -D " +self.parameters["device"] +" /opt/music/warning1.wav")
                self.ret["result"] = "failed"
                return self.ret
            else:
                usb_avg_val = usb_avg_val / usb_min_rms_counter
            usb_mic_array_rms.close()


            mic_array_wave = wave.open("/tmp/mic_array.wav","rb")
            chunk2 = mic_array_wave.readframes(mic_array_wave.getnframes())  
            data2 = np.fromstring(chunk2, dtype='int16')           
            #2，用snowboy对每个通道进行关键词检测
            for i in range(6):
                ans = detection.detector.RunDetection(np.array(data2[i::8], dtype=np.int16).tobytes())
                if ans == 1:
                    print('Hotword Detected!')
                else:
                    self.ret["result"] = str(i)
                    break
            mic_array_wave.close()

            #3，以1024的窗口对1-6通道进行rms测试，通道的最大值和最小值之差一定要合理的范围以内
            mic_array_rms = wave.open("/tmp/mic_array.wav","rb")

            chunk = mic_array_rms.readframes(CHUNK)

            while chunk != b'':
                min_rms = {"ch":99,"val":999999999}
                max_rms = {"ch":99,"val":0} 
                avg_val = 0            
                for ii in range(6):
                    data = np.fromstring(chunk, dtype='int16')
                    data = data[ii::8].tostring()
                    rms = audioop.rms(data, 2)

                    avg_val +=rms
                    #print('channel: {} RMS: {}'.format(ii,rms)) 
                    if min_rms["val"] > rms:
                        min_rms["val"] = rms
                        min_rms["ch"] = ii
                    if max_rms["val"] < rms:
                        max_rms["val"] = rms
                        max_rms["ch"] = ii
                       
                avg_val = avg_val/ii
                #4, rms是对静噪的测试，所以只考虑麦克风能力值平均值在600以内的窗
                if avg_val < 600:
                    print('max:',max_rms)                           
                    print('min:',min_rms)                           
                    if max_rms["val"]-min_rms["val"] > self.parameters["min"]:
                        self.ret["result"]="ch"+str(max_rms["ch"])+", ch"+str(min_rms["ch"])
                        break
                    avg_min_rms += min_rms["val"]
                    min_rms_counter += 1

                chunk = mic_array_rms.readframes(CHUNK)
            mic_array_rms.close()

            #如果1-6通道测试失败，直接返回，不进行下面的测试
            if self.ret["result"] != "ok":
                return self.ret

            #如果板载麦克风都测不到5段安静的声音，播放警告语音退出
            if min_rms_counter < 5:
                os.popen(" aplay -D " +self.parameters["device"] +" /opt/music/warning1.wav")
                self.ret["result"] = "failed"
                return self.ret

            #整体麦克风的灵敏度要在一定范围以内
            avg_min_rms = avg_min_rms / min_rms_counter
            usb_and_mic = avg_min_rms - usb_avg_val
            print("min_rms: ",usb_and_mic)
            if usb_and_mic  < avg_min_rm*self.parameters["min_rms"]:
                self.ret["result"] = "all error"
                return self.ret 


            #使用白噪声测试第7,8通道
            play_thread =threading.Thread(target=play_white,args=(self.parameters,))
            play_thread.start()      
            time.sleep(1)
            mic_array_thread =threading.Thread(target=mic_array_arecord,args=(self.parameters,))
            mic_array_thread.start()
            time.sleep(3)

            mic_array_rms = wave.open("/tmp/mic_array.wav","rb")

            chunk = mic_array_rms.readframes(CHUNK)

            while chunk != b'':
                avg_val = 0            
                for ii in range(2):
                    data = np.fromstring(chunk, dtype='int16')
                    data = data[6+ii::8].tostring()
                    rms = audioop.rms(data, 2)
                    #7,8通道统计rms
                    mic_rms[ii] = mic_rms[ii] + rms
                    counter = counter + 1
                    
                        
                chunk = mic_array_rms.readframes(CHUNK)

            for i in range(2):
                mic_rms[i] = mic_rms[i] / counter
                print('channel: {} RMS: {}'.format(i,mic_rms[i]))                           
                if i == 0:
                    if self.parameters["ch7"] - self.parameters["bias_c"] > mic_rms[i]  \
                    or self.parameters["ch7"] + self.parameters["bias_c"] < mic_rms[i]:
                        self.ret["result"] = "ch7"  
                        break
                if i == 1:
                    if self.parameters["ch8"] - self.parameters["bias_c"] > mic_rms[i]  \
                    or self.parameters["ch8"] + self.parameters["bias_c"] < mic_rms[i]:
                        self.ret["result"] = "ch8"
                        break           
        return self.ret
