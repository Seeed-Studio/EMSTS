from abc import ABCMeta, abstractmethod
import json
import importlib

class interface:
    __metaclass__ = ABCMeta

    def __init__(self, parameters):
        self.is_enable = parameters.get("status")
        self.is_thread = parameters.get("thread")

        
    def do_test(self):
        pass

    
class mainjob:
    def __init__(self):
        self.json_data = json.load(open("config.json",'r')) 
        self.interfaces  = [] 
        print(self.json_data)    
        
    def getjobs(self):
        for j in self.json_data:
            if j != "project" and j != "console":
                if self.json_data[j]["status"] == "okay":
                    self.interfaces.append(importlib.import_module("modules."+j+"."+j).subcore(self.json_data[j],self.json_data["project"]))
        return self.interfaces
    def getconsole(self):
        console =  importlib.import_module("modules.console."+self.json_data["console"]["file"])
        console.init(self.json_data["console"],self.json_data["project"])
        return console