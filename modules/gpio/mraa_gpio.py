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
import mraa
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
        self.input_io_group = []
        self.output_io_group = []

        for pin in parameters["input_io"]:
            self.input_io_group.append(mraa.Gpio(pin))
        for pin in self.input_io_group:
            #setup gpio input direction
            pin.dir(mraa.DIR_IN)   

        for pin in parameters["output_io"]:
            self.output_io_group.append(mraa.Gpio(pin))
        for pin in self.output_io_group:
            #setup gpio output direction
            pin.dir(mraa.DIR_OUT)   
          
    def do_test(self):
        #设置输出GPIO偶数为1，奇数为0
        counter = 0
        for pin in self.output_io_group:
            if counter%2 == 0:
                pin.write(1)
            else:
                pin.write(0)
            counter = counter + 1
        
        time.sleep(1)
        counter = 0
        #读取输入GPIO奇数和偶数的值跟输出GPIO相匹配
        for pin in self.input_io_group:
            if counter%2 == 0:
                if pin.read() != 1:
                    self.ret["result"] =  str(pin.getPin())
                    return self.ret
            else:
                if pin.read() != 0:
                    self.ret["result"] =  str(pin.getPin())
                    return self.ret
            counter = counter + 1

        #设置输出GPIO偶数为0，奇数为1
        counter = 0
        for pin in self.output_io_group:
            if counter%2 == 0:
                pin.write(0)
            else:
                pin.write(1)
            counter = counter + 1

        #读取输入GPIO奇数和偶数的值跟输出GPIO相匹配
        time.sleep(1)
        counter = 0
        for pin in self.input_io_group:
            if counter%2 == 0:
                if pin.read() != 0:
                    self.ret["result"] =  str(pin.getPin())
                    return self.ret
            else:
                if pin.read() != 1:
                    self.ret["result"] =  str(pin.getPin())
                    return self.ret
            counter = counter + 1


        return self.ret
