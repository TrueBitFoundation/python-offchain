import utils

class Linker(object):
    def __init__(self, modules):
        self.modules = modules

    def link(self):
        self.mergeFuncs()
        self.mergeGlobals()
        self.mergeDataSegs()
        self.resolveUndefinedExtern()

    def mergeFuncs(self):
        pass

    def mergeGlobals(self):
        pass

    def mergeDataSegs(self):
        pass

    def resolveUndefinedExtern(self):
        pass
