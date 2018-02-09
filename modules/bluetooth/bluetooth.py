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

# export LIBASOUND_THREAD_SAFE=0

import time
import pexpect
import subprocess
import sys
import os
import syslog



class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):                        
        f = file("./plog.out", 'w')
        subprocess.check_output("hcitool cmd 0x3F 0x01C 0x01 0x02 0x00 0x01 0x01", shell = True)
        # Start to open bluetoothctl
        self.child = pexpect.spawn("bluetoothctl")
        
        # TO-DO
        # If run bluetoothctl and can't get beaglebone MAC address, then reinitialize again
        
        self.child.logfile = f                                                   
            
    def __del__(self):
        self.child.sendline("quit")
        # print self.child.before
        self.child
        print "del function"
        
    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")



    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success



    def run_test(self,dist_mac_addr = "0C:A6:94:FB:16:38"):
        count =4
        status = 'error'   
        while count > 0 :
            print "connect to[1] : " + dist_mac_addr    
            self.child.sendline("connect " + dist_mac_addr)
            time.sleep(1)
            results = self.child.expect(["Connection successful", "Fail", "org.bluez.Error.Failed", pexpect.EOF,pexpect.TIMEOUT], timeout=10)
            print "connect speaker result: ",results
            if 0 < results:
                print "test whether connect ok?"
                time.sleep(4)
                self.child.sendline("info " + dist_mac_addr)
                time.sleep(1)
                results = self.child.expect(["Connected: yes", "Connected: no", pexpect.EOF,pexpect.TIMEOUT], timeout=5)
                if results > 0:
                    count = count -1
                else:
                    count = 0
            else:
                count = 0
        time.sleep(5)
        if dist_mac_addr=="0C:A6:94:FB:16:38" :     
            os.system("arecord -d 10 -D bluealsa:HCI=hci0,DEV=0C:A6:94:FB:16:38,PROFILE=sco /tmp/a.wav")
            os.system("aplay -D bluealsa:HCI=hci0,DEV=0C:A6:94:FB:16:38,PROFILE=a2dp /tmp/a.wav")

        time.sleep(1)
        #self.child.sendline("disconnect " + dist_mac_addr)
        status = 'ok'
        time.sleep(1.5)                    
        return status


   

if __name__ == "__main__":
    bl = Bluetoothctl()
    result = bl.run_test()
    print "bluetooth test result: ", result
  
