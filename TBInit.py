from utils import Colors, init_interpret
from OpCodes import WASM_OP_Code
from section_structs import Code_Section, Func_Body
from execute import *


# handles the debug option --memdump. dumps the contents of linear memories.
def DumpLinearMems(linear_memories, threshold):
    count = int()
    strrep = []
    linmem_cnt = int()
    for lin_mem in linear_memories:
        print('-----------------------------------------')
        print(Colors.blue + Colors.BOLD +
                'Linear Memory '+ repr(linmem_cnt)+ ' :' + Colors.ENDC)
        for byte in lin_mem:
            if count >= threshold:
                break
            if count%16 == 0:
                for ch in strrep:
                    # @DEVI-line feed messes the pretty format up
                    if ord(ch) != 10:
                        print(Colors.green + ' ' + ch + Colors.ENDC, end = '')
                    else:
                        pass
                print()
                strrep = []
                print(Colors.cyan + hex(count), ':\t' + Colors.ENDC, end='')
                strrep.append(str(chr(byte)))
                print(Colors.blue + format(byte, '02x') + ' ' + Colors.ENDC, end='')
            else:
                strrep += str(chr(byte))
                print(Colors.blue + format(byte, '02x') + ' ' + Colors.ENDC, end='')
            count += 1
        count = 0
    print()


# handles the debug options --idxspc. dumps the index spaces.
def DumpIndexSpaces(machinestate):
    print('-----------------------------------------')
    print(Colors.green + 'Function Index Space: ' + Colors.ENDC)
    for iter in machinestate.Index_Space_Function:
        print(Colors.blue + repr(iter) + Colors.ENDC)

    print('-----------------------------------------')
    print(Colors.green + 'Globa Index Space: ' + Colors.ENDC)
    for iter in machinestate.Index_Space_Global:
        print(Colors.blue + repr(iter) + Colors.ENDC)

    print('-----------------------------------------')
    print(Colors.green + 'Linear Memory Index Space: ' + Colors.ENDC)
    for iter in machinestate.Index_Space_Linear:
        print(Colors.blue + repr(iter) + Colors.ENDC)

    print('-----------------------------------------')
    print(Colors.green + 'Table Index Space: ' + Colors.ENDC)
    for iter in machinestate.Index_Space_Table:
        print(Colors.blue + repr(iter) + Colors.ENDC)
    print('-----------------------------------------')


# WIP-the Truebit Machine class
class TBMachine():
    def __init__(self):
        # bytearray of size PAGE_SIZE
        self.Linear_Memory = []
        self.Stack_Control_Flow = list()
        self.Stack_Call = list()
        self.Stack_Value = list()
        self.Stack_Omni = list()
        self.Vector_Globals = list()
        self.Index_Space_Function = list()
        self.Index_Space_Global = list()
        self.Index_Space_Linear = list()
        self.Index_Space_Table = list()


# handles the initialization of the WASM machine
class TBInit():
    def __init__(self, module, machinestate):
        self.module = module
        self.machinestate = machinestate

    # a convenience function that runs the methods of the class. all methods
    # can be called separately manually as well.
    def run(self):
        self.InitFuncIndexSpace()
        self.InitGlobalIndexSpace()
        self.InitLinearMemoryIndexSpace()
        self.InitTableIndexSpace()
        self.InitializeLinearMemory()

    def InitFuncIndexSpace(self):
        if self.module.import_section is not None:
            for iter in self.module.import_section.import_entry:
                if iter.kind == 0:
                    name = str()
                    for i in iter.field_str:
                        name += str(chr(i))
                    self.machinestate.Index_Space_Function.append(name)

        if self.module.function_section is not None:
            for iter in self.module.function_section.type_section_index:
                self.machinestate.Index_Space_Function.append(iter)

    def InitGlobalIndexSpace(self):
        if self.module.import_section is not None:
            for iter in self.module.import_section.import_entry:
                if iter.kind == 3:
                    name = str()
                    for i in iter.field_str:
                        name += str(chr(i))
                    self.machinestate.Index_Space_Global.append(name)

        if self.module.global_section is not None:
            for iter in self.module.global_section.global_variables:
                self.machinestate.Index_Space_Global.append(iter.init_expr)

    def InitLinearMemoryIndexSpace(self):
        if self.module.import_section is not None:
            for iter in self.module.import_section.import_entry:
                if iter.kind == 2:
                    name = str()
                    for i in iter.field_str:
                        name += str(chr(i))
                    self.machinestate.Index_Space_Linear.append(name)

        if self.module.memory_section is not None:
            for iter in self.module.memory_section.memory_types:
                self.machinestate.Index_Space_Linear.append(iter.initial)

    def InitTableIndexSpace(self):
        if self.module.import_section is not None:
            for iter in self.module.import_section.import_entry:
                if iter.kind == 1:
                    name = str()
                    for i in iter.field_str:
                        name += str(chr(i))
                    self.machinestate.Index_Space_Table.append(name)

        if self.module.table_section is not None:
            for iter in self.module.table_section.table_types:
                self.machinestate.Index_Space_Table.append(iter.element_type)

    def InitializeLinearMemory(self):
        # @DEVI-we could try to pack the data in the linear memory ourselve to
        # decrease the machinestate size
        if self.module.memory_section is not None:
            for iter in self.module.memory_section.memory_types:
                self.machinestate.Linear_Memory.append(bytearray(
                    WASM_OP_Code.PAGE_SIZE))
            if self.module.data_section is not None:
                for iter in self.module.data_section.data_segments:
                    count = int()
                    for byte in iter.data:
                        self.machinestate.Linear_Memory[iter.index][init_interpret(iter.offset) + count] = byte
                        count += 1



    # returns the machinestate
    def getInits(self):
        return(self.machinestate)


# WIP-holds the run-rime data structures for a wasm machine
class RTE():
    def __init__(self):
        Stack_Control_Flow = list()
        Stack_Value = list()
        Vector_Locals = list()
        Current_Position = int()
        Local_Stacks = list()

    def genFuncLocalStack(func_body):
        pass


# palceholder for the class that holds the validation functions
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

    def TBCustom(self):
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
        self.TBCustom()

        return(True)


# a convinience class that handles the initialization of the wasm machine and
# interpretation of the code.
class VM():
    def __init__(self, modules):
        self.modules = modules
        self.machinestate = TBMachine()
        # @DEVI-FIXME- the first implementation is single-module only
        self.init = TBInit(self.modules[0], self.machinestate)
        self.init.run()
        self.machinestate = self.init.getInits()
        self.start_function = Func_Body()
        self.executewasm = Execute(self.machinestate)

    def getState(self):
        return(self.machinestate)

    def getStartFunctionIndex(self):
        if self.modules[0].start_section is None:
            raise Exception(Colors.red + "module does not have a start section. quitting..." + Colors.ENDC)
        else:
            print(Colors.green + "found start section: " + Colors.ENDC, end = '')
            start_index = self.modules[0].start_section.function_section_index

        print(start_index)
        return(start_index)

    def getStartFunctionBody(self):
        start_index = self.getStartFunctionIndex()
        if isinstance(start_index, int):
            self.start_function = self.modules[0].code_section.func_bodies[start_index]
        elif isinstance(start_index, str):
            # we have to import the function from another module/library. we
            # assume sys calls are not present.:w
            pass
        else:
            raise Exception(Colors.red + "invalid entry for start function index" + Colors.ENDC)

    def execute(self):
        print(Colors.blue + 'running module...' + Colors.ENDC)
        '''
        for ins in self.start_function.code:
            print(ins.opcode + ' ' + ins.operands)
        '''
        for ins in self.start_function.code:
            self.executewasm.getInstruction(ins.opcodeint, ins.operands)
            self.executewasm.callExecuteMethod()
            self.getState()

    # a convinience method
    def run(self):
        self.getStartFunctionBody()
        self.execute()
