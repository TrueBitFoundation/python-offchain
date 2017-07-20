import argparser as agp


class TBMachine(object):
    def __init__(self):
        Linear_Memory = bytearray()
        Stack_Control_Flow = list()
        Stack_Call = list()
        Stack_Value = list()
        Vector_Globals = list()


class TBInit(object):
    def __init__(self):
        pass

    def run(self):
        self.ValidateModule()
        self.InitLinearMemory()
        self.InitTables()

    def ValidateModule(self):
        pass

    def InitLinearMemory(self):
        pass

    def InitTables(self):
        pass


class RTEnv(object):
    def __init__(self):
        Stack_Control_Flow = list()
        Stack_Value = list()
        Vector_Locals = list()
        Current_Position = int()
