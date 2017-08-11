import argparser as agp


class CSection(object):
    pass


class TBMachine(object):
    def __init__(self):
        Linear_Memory = bytearray()
        Stack_Control_Flow = list()
        Stack_Call = list()
        Stack_Value = list()
        Vector_Globals = list()
        Index_Space_Function = list()
        Index_Space_Global = list()
        Index_Space_Linear = list()
        Index_Space_Table = list()


class TBInit(object):
    def __init__(self):
        pass

    def run(self):
        self.ValidateModule()
        self.InitLinearMemory()
        self.InitTables()

    def InitLinearMemory(self):
        pass

    def InitTables(self):
        pass


class RTE(object):
    def __init__(self):
        Stack_Control_Flow = list()
        Stack_Value = list()
        Vector_Locals = list()
        Current_Position = int()


class ModuleValidation():
    def __init__(self, module):
        self.module = module

    def TypeSection(self):
        pass

    def ImportSection(self):
        pass

    def FunctionSection(self):
        pass

    def TableSection(self):
        pass

    def MemorySection(self):
        pass

    def GlobalSection(self):
        pass

    def ExportSection(self):
        pass

    def StartSection(self):
        pass

    def ElementSection(self):
        pass

    def CodeSection(self):
        pass

    def DataSection(self):
        pass

    def ValidateAll(self):
        self.TypeSection()
        self.ImportSection()
        self.FunctionSection()
        self.TableSection()
        self.MemorySection()
        self.GlobalSection()
        self.ExportSection()
        self.StartSection()
        self.ElementSection()
        self.CodeSection()
        self.DataSection()

        return(True)
