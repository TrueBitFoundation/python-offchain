import argparser as agp


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


class ValidateModule(object):
    def __init__(self, section_list):
        self.section_list = section_list

    def run(self):
        pass

    def validateTypeSection(self):
        pass

    def validateImportSection(self):
        pass

    def validateFunctionSection(self):
        pass

    def validateTableSection(self):
        pass

    def validateMemorySection(self):
        pass

    def validateGlobalSection(self):
        pass

    def validateExportSection(self):
        pass

    def validateStartSection(self):
        pass

    def validateElementSection(self):
        pass

    def validateCodeSection(self):
        pass

    def validateDataSection(self):
        pass
