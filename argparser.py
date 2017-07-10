from __future__ import print_function
import argparse
import sys
import re

__DBG__ = False


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class WASM_Byte_Code:
    control_flow_ops = [{'unreachable', '0x00'}, {'nop', '0x01'},
                        {'block', '0x02'}, {'loop', '0x03'},
                        {'if', '0x04'}, {'else', '0x05'},
                        {'end', '0x0b'}, {'br', '0x0c'},
                        {'br_if', '0x0d'}, {'br_table', '0x0e'},
                        {'return', '0x0f'}]

    call_ops = [{'call', '0x10'}, {'call_indirect', '0x11'}]

    param_ops = [{'drop', '0x1a'}, {'select', '0x1b'}]

    var_access = [{'get_local', '0x20'}, {'set_local', '0x21'},
                    {'tee_local', '0x22'}, {'get_global', '0x23'},
                    {'set_global', '0x24'}]

    mem_ops = [{'i32.load', '0x28'}, {'i64.load', '0x29'},
                {'f32.load', '0x2a'}, {'f64.load', '0x2b'},
                {'i32.load8_s', '0x2c'}, {'i32.load8_u', '0x2d'},
                {'i32.load16_s', '0x2e'},  {'i32.load16_u', '0x2f'},
                {'i64.load8_s', '0x30'}, {'i64.load8_u', '0x31'},
                {'i64.load16_s', '0x32'}, {'i64.load16_u', '0x33'},
                {'i64.load32_s', '0x34'}, {'i64.load32_u', '0x35'},
                {'i32.store', '0x36'}, {'i64.store', '0x37'},
                {'f32.store', '0x38'}, {'f64.store', '0x39'},
                {'i32.store8', '0x3a'}, {'i32.store16', '0x3b'},
                {'i64.store8', '0x3c'}, {'i64.store16', '0x3d'},
                {'i64.store32', '0x3e'}, {'current_memory', '0x3f'},
                {'grow_memory', '0x40'}]

    consts = [{'i32.const', '0x41'}, {'i64.const', '0x42'},
              {'f32.const', '0x43'}, {'f64', '0x44'}]

    comp_ops = [{'i32.eqz', '0x45'}, {'i32.eq', '0x46'}, {'i32.ne', '0x47'},
                {'i32.lt_s', '0x48'}, {'i32.lt_u', '0x49'},
                {'i32.gt_s', '0x4a'}, {'i32.gt_u', '0x4b'},
                {'i32.le_s', '0x4c'}, {'i32.le_u', '0x4d'},
                {'i32.ge_s', '0x4e'}, {'i32.ge_u', '0x4f'},
                {'i64.eqz', '0x50'}, {'i64.eq', '0x51'},
                {'i64.ne', '0x52'}, {'i64.lt_s', '0x53'},
                {'i64.lt_u', '0x54'}, {'i64.gt_s', '0x55'},
                {'i64.gt_u', '0x56'}, {'i64.le_s', '0x57'},
                {'i64.le_u', '0x58'}, {'i64.ge_s', '0x59'},
                {'i64.ge_u', '0x5a'}, {'f32.eq', '0x5b'},
                {'f32.ne', '0x5c'}, {'f32.lt', '0x5d'},
                {'f32.gt', '0x5e'}, {'f32.le', '0x5f'},
                {'f32.ge', '0x60'}, {'f64.eq', '0x61'},
                {'f64.ne', '0x62'}, {'f64.lt', '0x63'},
                {'f64.gt', '0x64'}, {'f64.le', '0x65'},
                {'f64.ge', '0x66'}]

    num_ops = [{'i32.clz', '0x67'}, {'i32.ctz', '0x68'},
               {'i32.popcnt', '0x69'}, {'i32.add', '0x6a'},
               {'i32.sub', '0x6b'}, {'i32.mul', '0x6c'},
               {'i32.div_s', '0x6d'}, {'i32.div_u', '0x6e'},
               {'i32.rem_s', '0x6e'}, {'i32.rem_u', '0x70'},
               {'i32.and', '0x71'}, {'i32.or', '0x72'},
               {'i32.xor', '0x73'}, {'i32.shl', '0x74'},
               {'i32.shr_s', '0x75'}, {'i32.shr_u', '0x76'},
               {'i32.rotl', '0x77'}, {'i32.rotr', '0x78'},
               {'i64.clz', '0x79'}, {'i64.ctz', '0x7a'},
               {'i64.popcnt', '0x7b'}, {'i64.add', '0x7c'},
               {'i64.sub', '0x7d'}, {'i64.mul', '0x7e'},
               {'i64.div_s', '0x7f'}, {'i64.div_u', '0x80'},
               {'i64.rem_s', '0x81'}, {'i64.rem_u', '0x82'},
               {'i64.and', '0x83'}, {'i64.or', '0x84'},
               {'i64.xor', '0x85'}, {'i64.shl', '0x86'},
               {'i64.shr_s', '0x87'}, {'i64.shr_u', '0x88'},
               {'i64.rotl', '0x89'}, {'i63.rotr', '0x8a'},
               {'f32.abs', '0x8b'}, {'f32.neg', '0x8c'},
               {'f32.ceil', '0x8d'},  {'f32.floor', '0x8e'},
               {'f32.trunc', '0x8f'}, {'f32.nearest', '0x90'},
               {'f32.sqrt', '0x91'}, {'f32.add', '0x92'},
               {'f32.sub', '0x93'}, {'f32.mul', '0x94'},
               {'f32.div', '0x95'}, {'f32.min', '0x96'},
               {'f32.max', '0x97'}, {'f32.copysign', '0x98'},
               {'f64.abs', '0x99'}, {'f64.neg', '0x9a'},
               {'f64.ceil', '0x9b'}, {'f64.floor', '0x9c'},
               {'f64.trunc', '0x9d'}, {'f64.nearest', '0x9e'},
               {'f64.sqrt', '0x9f'}, {'f64.add', '0xa0'},
               {'f64.sub', '0xa1'}, {'f64.mul', '0xa2'},
               {'f64.div', '0xa3'}, {'f64.min', '0xa4'},
               {'f64.max', '0xa5'}, {'f64.copysign', '0xa6'}]

    conversion = [{'i32.wrap/i64', '0xa7'},
                    {'i32.wrap/i64', '0xa7'},
                    {'i32.trunc_s/f32', '0xa8'},
                    {'i32.trunc_u/f32', '0xa9'},
                    {'i32.trunc_s/f64', '0xaa'},
                    {'i32.trunc_u/f64', '0xab'},
                    {'i64.extend_s/i32', '0xac'},
                    {'i64.extend_u/i32', '0xad'},
                    {'i64.trunc_s/f32', '0xae'},
                    {'i64.trunc_u/f32', '0xaf'},
                    {'i64.trunc_s/f64', '0xb0'},
                    {'i64.trunc_u/f64', '0xb1'},
                    {'f32.convert_s/i32', '0xb2'},
                    {'f32.convert_u/i32', '0xb3'},
                    {'f32.convert_s/i64', '0xb4'},
                    {'f32.convert_u/i64', '0xb5'},
                    {'f32.demote/f64', '0xb6'},
                    {'f64.convert_s/i32', '0xb7'},
                    {'f64.convert_u/i32', '0xb8'},
                    {'f64.convert_s/i64', '0xb9'},
                    {'f64.convert_u/i64', '0xba'},
                    {'f64.promote/f32', '0xbb'}]

    reinterpretations = [{'i32.reinterpret/f32','0xbc'},
                         {'i64.reinterpret/f64','0xbd'},
                         {'f32.reinterpret/i32','0xbe'},
                         {'f64.reinterpret/i64','0xbf'}]


class CLIArgParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--wasm", type=str,
                            help="path to the wasm test file")
        self.args = parser.parse_args()
        if self.args.wasm is None:
            raise Exception('empty wasm text file path')

    def getWASMTPath(self):
        return self.args.wasm


class WASMText(object):
    wast_header_type = dict()
    wast_header_import = dict()
    wast_header_table = dict()
    wast_header_elem = dict()
    wast_header_memory = dict()
    wast_header_data = dict()
    wast_header_export = dict()
    wast_header_func = dict()
    wast_func_bodies = dict()

    def __init__(self, file_path):
        self.wasmt_file = open(file_path, "r")
        self.file_path = file_path
        self.test_file = open("./test.txt", "a")

    def write(self, text):
        self.wasmt_file.write(text)

    def reopen_for_read(self):
        self.wasmt_file.close()
        self.wasmt_file.open(self.file_path, "r")

    def reopen_for_write(self):
        self.wasmt_file.close()
        self.wasmt_file.open(self.file_path, "w")

    def test_print(self):
        for line in self.wasmt_file:
            print(line, file=self.test_file)
            sys.stdout.write(line)
            sys.stdout.write('\n')

    def RegExSearch(self):
        # pattern1 = re.compile('^\(type\ \$[a-zA-Z0-9]+\$[v|i]+\ \(func$\)')
        pattern1 = re.compile('[ \t]+\(type.+\)')
        # pattern1 = re.compile('[a-zA-Z0-9]+')
        pattern2 = re.compile('[ \t]+\(import.+\)')
        pattern3 = re.compile('[ \t]+\(table.+\)')
        pattern4 = re.compile('[ \t]+\(elem.+\)')
        pattern5 = re.compile('[ \t]+\(memory.+\)')
        pattern6 = re.compile('[ \t]+\(data.+\)')
        pattern7 = re.compile('[ \t]+\(export.+\)')
        pattern8 = re.compile('[ \t]+\(func.+\)')

        linenumber = 0

        for line in self.wasmt_file:
            # print(line)
            linenumber += 1
            result = re.match(pattern1, line)
            if result is not None:
                self.wast_header_type[linenumber] = line
            result = re.match(pattern2, line)
            if result is not None:
                self.wast_header_import[linenumber] = line
            result = re.match(pattern3, line)
            if result is not None:
                self.wast_header_table[linenumber] = line
            result = re.match(pattern4, line)
            if result is not None:
                self.wast_header_elem[linenumber] = line
            result = re.match(pattern5, line)
            if result is not None:
                self.wast_header_memory[linenumber] = line
            result = re.match(pattern6, line)
            if result is not None:
                self.wast_header_data[linenumber] = line
            result = re.match(pattern7, line)
            if result is not None:
                self.wast_header_export[linenumber] = line
            result = re.match(pattern8, line)
            if result is not None:
                self.wast_header_func[linenumber] = line

    def FuncParser(self):
        parentheses_cnt = 0
        func_cnt = 0
        funcbody = str()
        pos = 0
        for key in self.wast_header_func:
            self.wasmt_file.seek(0, 0)
            parentheses_cnt = 0
            i = 0
            alive = False
            for line in self.wasmt_file:
                i += 1
                if i == key or alive:
                    func_cnt += 1
                    funcbody += line

                    pos = line.find('(', pos, len(line))
                    while(pos != -1):
                        parentheses_cnt += 1
                        pos = line.find('(', pos + 1, len(line))
                    pos = 0

                    pos = line.find(')', pos, len(line))
                    while(pos != -1):
                        parentheses_cnt -= 1
                        pos = line.find('(', pos + 1, len(line))
                    pos = 0

                    if parentheses_cnt == 0:
                        self.wast_func_bodies[func_cnt] = funcbody
                        func_cnt = 0
                        parentheses_cnt = 0
                        funcbody = ""
                        alive = False
                        break
                    elif parentheses_cnt > 0:
                        # we need to parse another line
                        alive = True
                        continue
                    else:
                        # parentheses_cnt < 0. the wasmt file is malformed.
                        raise Exception('malformed: mismatching number \
                                        of parentheses')

    def FuncParserTest(self):
        for k in self.wast_func_bodies:
            print(self.wast_func_bodies[k])

    def PrintTypeDict(self):
        for element in self.wast_header_type:
            # print(self.wast_header_type[element])
            print(Colors.OKGREEN + self.wast_header_type[element] + Colors.ENDC)

    def PrintImportDict(self):
        for element in self.wast_header_import:
            print(Colors.FAIL + self.wast_header_import[element] + Colors.ENDC)

    def PrintTableDict(self):
        for element in self.wast_header_table:
            print(Colors.HEADER + self.wast_header_table[element] + Colors.ENDC)

    def PrintElemDict(self):
        for element in self.wast_header_elem:
            print(Colors.OKBLUE + self.wast_header_elem[element] + Colors.ENDC)

    def PrintMemoryDict(self):
        for element in self.wast_header_memory:
            print(Colors.UNDERLINE + self.wast_header_memory[element] +
                  Colors.ENDC)

    def PrintDataDict(self):
        for element in self.wast_header_data:
            print(Colors.WARNING + self.wast_header_data[element] + Colors.ENDC)

    def PrintExportDict(self):
        for element in self.wast_header_export:
            print(Colors.BOLD + self.wast_header_export[element] + Colors.ENDC)

    def PrintFuncDict(self):
        for element in self.wast_header_func:
            print(Colors.HEADER + self.wast_header_func[element] + Colors.ENDC)

    def getTypeHeader(self):
        return self.wast_header_type

    def getImportHeader(self):
        return self.wast_header_import

    def getTableHeader(self):
        return self.wast_header_table

    def getElemHeader(self):
        return self.wast_header_elem

    def getMemoryHeader(self):
        return self.wast_header_memory

    def getDataHeader(self):
        return self.wast_header_data

    def getExportHeader(self):
        return self.wast_header_export

    def getFuncHeader(self):
        return self.wast_header_func

    def getFuncBodies(self):
        return self.wast_func_bodies

    def __del__(self):
        self.test_file.close()
        self.wasmt_file.close()


class FuncBodyParser(object):
    wast_obj_func = dict()

    def __init__(self, wast_obj_func):
        self.wast_obj_func = wast_obj_func

    def ParseBody(self):
        pos = 0
        lastopenparen = 0

        for funcbody in self.wast_obj_func:
            for line in funcbody:
                parentheses_cnt = 0
                pos = line.find('(', pos, len(line))
                lastopenparen = pos
                while(pos != -1):
                    parentheses_cnt += 1
                    pos = line.find('(', pos + 1, len(line))
                    lastopenparen
                pos = 0

                pos = line.find(')', pos, len(line))
                while(pos != -1):
                    parentheses_cnt -= 1
                    pos = line.find('(', pos + 1, len(line))
                pos = 0

                if parentheses_cnt == 0:
                    parentheses_cnt = 0
                    break
                elif parentheses_cnt > 0:
                    # we need to parse another line
                    continue
                else:
                    # parentheses_cnt < 0. the wasmt file is malformed
                    print("goofball")

    def ParseBodyV2(self):
        sexpr_pattern = re.compile('\([^(]*?\)')

        for funcbody in self.wast_obj_func:
            print(Colors.OKBLUE + self.wast_obj_func[funcbody] + Colors.ENDC)

            most_concat_sexpr = re.findall(sexpr_pattern,
                                           self.wast_obj_func[funcbody])
            print ('-----------------------------')

            for elem in most_concat_sexpr:
                print(elem)
                print ('-----------------------------')
                elem.split

    def ParseBodyV3(self):
        stack = []
        one_line = []
        sexpr_greedy = re.compile('\s*(?:(?P<lparen>\()|(?P<rparent>\))|(?P<operandnum>[i|ui][0-9]+$)|(?P<regarg>\$[0-9]+$)|(?P<keyword>[a-zA-Z0-9\._]+)|(?P<identifier>[\$][a-zA-Z0-9_\$]+))')

        for funcbody in self.wast_obj_func:
            for stackval in re.finditer(sexpr_greedy,
                                        self.wast_obj_func[funcbody]):
                for k, v in stackval.groupdict().items():
                    if v is not None:
                        print(k, v)


class ParserV1(object):
    def run(self):
        argparser = CLIArgParser()
        wasmtobj = WASMText(argparser.getWASMTPath())
        # wasmtobj.test_print()
        wasmtobj.RegExSearch()
        if __DBG__:
            wasmtobj.PrintTypeDict()
            wasmtobj.PrintImportDict()
            wasmtobj.PrintTableDict()
            wasmtobj.PrintElemDict()
            wasmtobj.PrintMemoryDict()
            wasmtobj.PrintDataDict()
            wasmtobj.PrintExportDict()
            wasmtobj.PrintFuncDict()
            wasmtobj.PrintElemDict()
        wasmtobj.FuncParser()
        if __DBG__:
            wasmtobj.FuncParserTest()
        funcbodyparser = FuncBodyParser(wasmtobj.getFuncBodies())
        funcbodyparser.ParseBodyV3()


def main():
    parser = ParserV1()
    parser.run()


if __name__ == '__main__':
    main()
