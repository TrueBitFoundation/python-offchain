#!/bin/python3.5

# call it the regression testing file
import sys
import os
from test_LEB128 import test_signed_LEB128
from test_LEB128 import test_unsigned_LEB128
sys.path.append('../')
from utils import Colors
from argparser import ObjReader

total_test_cnt = int()
expected_pass_cnt = int()
expected_fail_cnt = int()

success = Colors.green + "SUCCESS: " + Colors.ENDC
fail = Colors.red + "FAIL: " + Colors.ENDC


def ObjectList():
    obj_list = []
    cwd = os.getcwd()
    for file in os.listdir(cwd + "/testsuite"):
        if file.endswith(".wasm"):
            obj_list.append(cwd + "/testsuite/" + file)

    return(obj_list)


def main():
    return_list = []
    # LEB128 tests
    test_unsigned_LEB128()
    test_signed_LEB128()
    # parser test on the WASM testsuite
    obj_list = ObjectList()
    for testfile in obj_list:
        pid = os.fork()
        # I dont have a bellybutton
        if pid == 0:
            # @DEVI-FIXME- the dbg option in argparser is not working yet
            # if you want to pipe this, run with python -u
            sys.stdout = open('/dev/null', 'w')
            sys.stderr = open('/dev/null', 'w')

            wasmobj = ObjReader(testfile, 'little', False, False)
            wasmobj.ReadWASM()
            wasmobj.ReadCodeSection()
            wasmobj.ReadDataSection()
            wasmobj.ReadImportSection()
            wasmobj.ReadSectionExport()
            wasmobj.ReadSectionType()
            wasmobj.ReadSectionFunction()
            wasmobj.ReadSectionElement()
            wasmobj.ReadMemorySection()
            wasmobj.ReadSectionTable()
            wasmobj.ReadSectionGlobal()
            wasmobj.ReadStartSection()
            sys.exit()
        # the parent process
        elif pid > 0:
            cpid, status = os.waitpid(pid, 0)
            return_list.append(status)
            # @DEVI-FIXME- if you pipe it its broken
            if status == 0:
                print(success + testfile)
            else:
                print(fail + testfile)
        else:
            # badically we couldnt fork a child
            print(fail + 'return code:' + pid)
            raise Exception("could not fork child")


if __name__ == '__main__':
    main()
