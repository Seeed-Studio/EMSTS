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
import time
from kernel import core

class subcore(core.interface):
    def __init__(self,parameters,platform,debug):
        super(subcore,self).__init__(parameters)
        self.parameters = parameters
        self.platform = platform
        self.debug = debug
        self.ret = {
            "description": self.parameters["description"],
            "result": "failed"
        }
    def do_test(self):
        try:
            nr_sectors = open('/sys/block/'+self.parameters["location"]+'/size').read().rstrip('\n')
            sect_size = open('/sys/block/'+self.parameters["location"]+'/queue/hw_sector_size').read().rstrip('\n')
        except :
            self.ret["result"] = "failed"

        real_size =  float(nr_sectors)*float(sect_size)/(1024.0*1024.0*1024.0)

        if self.parameters["size"] - self.parameters["bias"] < real_size  \
        and self.parameters["size"] + self.parameters["bias"] > real_size:
            self.ret["result"] = "ok"

        return self.ret
