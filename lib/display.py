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
#
# +-------------------------------------+-----------------------+
# Test item: ok|                        |                       |
# Test item: ok|                        |                       |
# Test item: ok|                        |                       |
# Test item: ok|   PIC1                 |    PIC2               |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            |                        |                       |
# |            +------------------------+-----------------------+
# |            |                                                |
# |            |         finish(failed or succeed)              |
# |            |                                                |
# +------------+------------------------------------------------+



import time
import os
import pygame, sys
from pygame.locals import *
import queue
import threading

class display(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #Set up pygame
        pygame.init()
        self.screen_info = pygame.display.Info()
        self.hight = self.screen_info.current_h
        self.wide = self.screen_info.current_w
        self.text_index = 0
        self.pic_w = self.wide / 3 + 150
        self.pic_h = self.hight*2/3
        #Set up the window
        self.windowSurface = pygame.display.set_mode((self.wide, self.hight), 0 , 32)
        pygame.display.set_caption('ReSpeaker v2')

        #Set up the colors
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.WHITE = (255,255,255)

        #Draw the white background onto the surface
        self.windowSurface.fill(self.BLACK)

        self.isExit = True
        self.data = queue.Queue()
    def run(self):
        while self.isExit:
            if not self.data.empty():
                latest_data = self.data.get()
                if latest_data["type"] == "text":
                    self.print_text(latest_data)
                elif latest_data["type"] == "picture":
                    if latest_data["location"] == "left":
                        self.print_pic_left(latest_data["path"])
                    else:
                        self.print_pic_right(latest_data["path"])
                elif latest_data["type"] == "finish":
                    self.print_finish(latest_data["finish"])
                self.show()
                print(latest_data)

    def show(self):
        #Draw the window onto the screen
        pygame.display.update()

    def print_text(self,str_line):
        self.print_str(str_line["description"]+": ",self.BLUE,50,20,20 + self.text_index*35)
        if str_line["result"] == "ok":
            #len("ok") == 2
            self.print_str(str_line["result"],self.GREEN,50,320 - 20 - 16*2,20 + self.text_index*35)
        elif str_line["result"] == "failed":
             #len("failed") == 6
            self.print_str(str_line["result"],self.RED,50,320 - 20 - 16*6,20 + self.text_index*35)
        elif str_line["result"] == "listen":
            #len("listen") == 6
            self.print_str(str_line["result"],self.WHITE,50,320 - 20 - 16*6,20 + self.text_index*35)
        else :
            #len("watch") = 5
            self.print_str(str_line["result"],self.WHITE,50,320 - 20 - 16*5,20 + self.text_index*35)
        self.text_index = self.text_index + 1

    #very char use 15bit    
    def print_str(self,str,color,f_size,x,y):
        f = pygame.font.Font(None, f_size)
        w,h = f.size(str)
        #print('wide: {} hight: {} '.format(w,h))
        pygame.draw.rect(self.windowSurface,self.BLACK,(x,y,320,h))

        text_surface = f.render(str, True, color)

        self.windowSurface.blit(text_surface, (x, y)) 
    def print_pic_right(self,pic="/opt/pic/rgb.png"):
        picture = pygame.image.load(pic)
        picture = pygame.transform.scale(picture, (int(self.pic_w), int(self.pic_h)))    
        rect = picture.get_rect() 
        rect = rect.move((self.wide - self.pic_w, 20 ))
        self.windowSurface.blit(picture, rect)  

    def print_pic_left(self,pic="/opt/pic/rgb.png"):
        picture = pygame.image.load(pic)
        picture = pygame.transform.scale(picture, (int(self.pic_w), int(self.pic_h)))   
        rect = picture.get_rect() 
        rect = rect.move((int(self.wide-self.pic_w*2) -5 , 20 ))
        self.windowSurface.blit(picture, rect)     
    

    def print_finish(self,r):
        if r == True:
            self.print_str(u"SUCCEED",self.GREEN,300,self.wide-1.5*self.pic_w , (self.hight + self.pic_h)/2 - 80)
        else:
            self.print_str(u"FAILED",self.RED,300,self.wide-1.5*self.pic_w, (self.hight + self.pic_h)/2 - 80)
    def __del__(self):
        self.isExit = False
        pygame.quit()
    
if __name__ == "__main__":
    data_json = {}
    d = display()
    d.start()
    data_json.clear()
    data_json["type"] = "text"
    data_json["description"] = "221223"
    data_json["result"] = "ok"
    d.data.put(data_json)

    time.sleep(0.1)
    data_json.clear()
    data_json["type"] = "text"
    data_json["description"] = "4525434"
    data_json["result"] = "failed"
    d.data.put(data_json)

    time.sleep(0.1)
    data_json.clear()
    data_json["type"] = "text"
    data_json["description"] = "8678657"
    data_json["result"] = "watch"
    d.data.put(data_json)

    time.sleep(0.1)
    data_json.clear()
    data_json["type"] = "text"
    data_json["description"] = "adfsdf"
    data_json["result"] = "listen"
    d.data.put(data_json)    

    time.sleep(3)
    data_json.clear()
    data_json["type"] = "picture"
    data_json["path"] = "/opt/pic/logo.png"
    data_json["location"] = "left"
    d.data.put(data_json)

    time.sleep(3)
    data_json.clear()
    data_json["type"] = "picture"
    data_json["path"] = "/opt/pic/speaker.png"
    data_json["location"] = "right"
    d.data.put(data_json)

    time.sleep(3)
    data_json.clear()
    data_json["type"] = "finish"
    data_json["finish"] = True
    d.data.put(data_json)

    time.sleep(3)
    data_json.clear()
    data_json["type"] = "finish"
    data_json["finish"] = False
    d.data.put(data_json)


    time.sleep(10)    
