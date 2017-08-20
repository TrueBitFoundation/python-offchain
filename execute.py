from OpCodes import *


def instructionUnwinder(opcode, immediates, machinestate):
    pass


class Execute():
    def __init__(self, machinestate):
        self.machinestate = machinestate
        self.opcode = ''
        self.immediates = []

    def getInstruction(self, opcode, immediates):
        self.opcode = opcode
        self.immediates = immediates


    def callExecuteMethod(self):
        instructionUnwinder(opcode, immediates, machinestate)

    def run_const(opcode, immediates):
        pass

    def run_getlocal(opcode, immediates):
        pass

    def run_setlocal(opcode, immediates):
        pass

    def run_teelocal(opcode, immediates):
        pass

    def run_getglobal(opcode, immediates):
        pass

    def run_setglobal(opcode, immediates):
        pass

    def run_call(opcode, immediates):
        pass
