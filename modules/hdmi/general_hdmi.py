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

# export SDL_NOMOUSE=1
from kernel import core
import time
import os
import pygame, sys
from pygame.locals import *

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
    def do_test(self):
        #Set up pygame
        pygame.init()
        screen_info = pygame.display.Info()
        hight = screen_info.current_h
        wide = screen_info.current_w
        #Set up the window
        windowSurface = pygame.display.set_mode((wide, hight), 0 , 32)
        pygame.display.set_caption('ReSpeaker v2')

        #Set up the colors
        BLACK = (0,0,0)
        RED = (255,0,0)
        GREEN = (0,255,0)
        BLUE = (0,0,255)
        WHITE = (255,255,255)

        #Set up fonts
        basicFont = pygame.font.SysFont(None, 80)

        #Set up the text
        text = basicFont.render('RESPEAKER TEST', True, WHITE)
        textRect = text.get_rect()
        textRect.centerx = windowSurface.get_rect().centerx
        textRect.centery = windowSurface.get_rect().centery

        #Draw the white background onto the surface
        windowSurface.fill(WHITE)

        #Draw a blue poligon onto the surface
        pygame.draw.polygon(windowSurface, BLUE, ((wide/2, 0), (wide,hight/2),(wide/2,hight), (0,hight*0.5) ))

        #Draw a green poligon onto the surface
        pygame.draw.polygon(windowSurface, GREEN, ((0.25*wide,0.25*hight),(0.75*wide,0.25*hight),(0.75*wide,0.75*hight),(0.25*wide,0.75*hight)))

        #Draw a red circle onto the surface
        pygame.draw.circle(windowSurface, RED, (int(0.5*wide),int(0.5*hight)), int(0.25*wide))

        #Get a pixel array of the surface
        pixArray = pygame.PixelArray(windowSurface)
        pixArray[480][380] = BLACK
        del pixArray

        #Draw the text onto the surface
        windowSurface.blit(text,textRect)

        #Draw the window onto the screen
        pygame.display.update()

        #Run the game loop
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == QUIT:
        #             pygame.quit()
        #             sys.exit()
        time.sleep(10)
        pygame.quit()

        return self.ret






