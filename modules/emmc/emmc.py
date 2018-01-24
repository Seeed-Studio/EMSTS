
from kernel import core
import importlib

class subcore(core.interface):
    def __init__(self,parameters,platform):
        #core.interface.__init__(self,parameters)
        super(subcore,self).__init__(parameters)
        self.t_emmc = importlib.import_module("modules.emmc."+parameters["file"])
        self.t_emmc.init(parameters,platform)
    def do_test(self):
        return self.t_emmc.do_test() 