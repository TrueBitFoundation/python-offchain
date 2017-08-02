import sys
from test_LEB128 import test_signed_LEB128
from test_LEB128 import test_unsigned_LEB128
sys.path.append('../')
from utils import *
from argparser import ObjReader
import os


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
    #LEB128 tests
    test_unsigned_LEB128()
    test_signed_LEB128()
    obj_list = ObjectList()
    #parser test on the WASM testsuite
    for testfile in obj_list:
        wasmobj = ObjReader(testfile, 'little', False)
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


if __name__ == '__main__':
    main()
