from kernel import core
import importlib

class subcore(core.interface):
    def __init__(self,parameters,platform):
        #core.interface.__init__(self,parameters)
        super(subcore,self).__init__(parameters)
        self.t_eth = importlib.import_module("modules.eth."+parameters["file"])
        self.t_eth.init(parameters,platform)
    def do_test(self):
        return self.t_eth.do_test() 