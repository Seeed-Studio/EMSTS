
from kernel import core
import importlib

class subcore(core.interface):
    def __init__(self,parameters,platform):
        #core.interface.__init__(self,parameters)
        super(subcore,self).__init__(parameters)
        self.t_ddr = importlib.import_module("modules.ddr."+parameters["file"])
        self.t_ddr.init(parameters,platform)
    def do_test(self):
        self.t_ddr.do_test() 