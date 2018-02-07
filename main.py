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
import threading
import signal

def do_thread(fun,console,e):
    print("********")
    ret = fun()
    console.log(ret)
    if ret["result"] != "ok":
        e.set()
    


if __name__ == "__main__":
    interfaces = core.mainjob()
    jobs = interfaces.getjobs()
    console = interfaces.getconsole()
    e = threading.Event()
    ts = []


    for j in jobs:
        if j.is_thread ==  "okay":
            t =threading.Thread(target=do_thread,args=(j.do_test,console,e,))
            t.start()
            ts.append(t)

    for i in jobs:
        if i.is_thread !=  "okay":
            ret = i.do_test()
            console.log(ret)
            print("========")
            if ret["result"] != "ok" or e.wait(1):
                for ii in ts:
                    ii.join()               
                break

    #console.log("%o" % 20)
   
