#!/bin/python3.5

# call it the regression testing file
# @DEVI-if you wanna pipe the output, run with python -u. buffered output
# screws up the output

import sys
import os
from test_LEB128 import test_signed_LEB128
from test_LEB128 import test_unsigned_LEB128
from leb128s import leb128sencodedecodeexhaustive
from leb128s import leb128uencodedecodeexhaustive
from abc import ABCMeta, abstractmethod
sys.path.append('../')
from utils import Colors
from argparser import *
from TBInit import *

total_test_cnt = int()
expected_pass_cnt = int()
expected_fail_cnt = int()

success = Colors.green + "SUCCESS: " + Colors.ENDC
fail = Colors.red + "FAIL: " + Colors.ENDC


# in order to keep the regression test script clean, the tests will need to
# inherit from this test class, implement the two virtual methods and then call
# it inside the main.
class Void_Spwner():
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    # this is the method that runs your tests
    @abstractmethod
    def Legacy(self):
        pass

    # this tells the class what name to use to display your test results
    @abstractmethod
    def GetName(self):
        return(str())

    def Spwn(self):
        pid = os.fork()

        # I don't have a bellybutton
        if pid == 0:
            self.Legacy()
            sys.exit()
        elif pid > 0:
            cpid, status = os.waitpid(pid, 0)
            if status == 0:
                print(success + ': ' + self.GetName())
            else:
                print(fail + ': ' + self.GetName())
        else:
            # basically we couldnt fork a child
            print(fail + 'return code:' + pid)
            raise Exception("could not fork child")


def ObjectList():
    obj_list = []
    cwd = os.getcwd()
    for file in os.listdir(cwd + "/testsuite"):
        if file.endswith(".wasm"):
            obj_list.append(cwd + "/testsuite/" + file)

    return(obj_list)

################################################################################
class LEB128EncodeTest(Void_Spwner):
    def Legacy(self):
        test_unsigned_LEB128()
        test_signed_LEB128()

    def GetName(self):
        return('leb128encodetest')

class LEB128Exhaustive(Void_Spwner):
    def Legacy(self):
        leb128sencodedecodeexhaustive()
        leb128uencodedecodeexhaustive()

    def GetName(self):
        return('leb128exhaustive')

################################################################################
def main():
    return_list = []
    # LEB128 tests
    leb128encodetest = LEB128EncodeTest()
    leb128encodetest.Spwn()
    # leb128s exhaustive
    leb128sex = LEB128Exhaustive()
    leb128sex.Spwn()
    # parser test on the WASM testsuite
    obj_list = ObjectList()
    for testfile in obj_list:
        pid = os.fork()
        # I dont have a bellybutton
        if pid == 0:
            # @DEVI-FIXME-pipe stdout and stderr to a file instead of the
            # bitbucket
            sys.stdout = open('/dev/null', 'w')
            sys.stderr = open('/dev/null', 'w')

            interpreter = PythonInterpreter()
            module = interpreter.parse(testfile)
            interpreter.appendmodule(module)
            interpreter.dump_sections(module)
            interpreter.runValidations()
            vm = VM(interpreter.getmodules())
            ms = vm.getState()
            # interpreter.dump_sections(module)
            DumpIndexSpaces(ms)
            DumpLinearMems(ms.Linear_Memory, 1000)
            sys.exit()
        # the parent process
        elif pid > 0:
            # @DEVI-FIXME-we are intentionally blocking. later i will fix this
            # so we can use multicores to run our reg tests faster.
            cpid, status = os.waitpid(pid, 0)
            return_list.append(status)
            if status == 0:
                print(success + testfile)
            else:
                print(fail + testfile)
        else:
            # basically we couldnt fork a child
            print(fail + 'return code:' + pid)
            raise Exception("could not fork child")


if __name__ == '__main__':
    main()
