#!/bin/python3

from __future__ import print_function
import argparse
import sys
import re
from section_structs import *
from utils import *
from OpCodes import *
from copy import deepcopy
from TBInit import *
from merklize import *

_DBG_ = True


# we first read the object file and put all the sections in this class
class ParsedStruct:
    def __init__(self):
        self.version_number = int()
        self.section_list = []


# like the above. currently unused
class ParsedStructV2:
    def __init__(self, version_number, section_list):
        self.version_number = version_number
        self.section_list = section_list


# @DEVI-Deprecated-convert a bytearray to int
def Conver2Int(little_endian, size, bytelist):
    modifier = size - 1
    sum = 0

    if little_endian:
        for bit in reversed(bytelist):
            if bit != 0x80:
                sum += bit*(pow(16, modifier))
            modifier -= 1
        return(sum)
    else:
        for bit in reversed(bytelist):
            if bit != 0x80:
                sum += bit*(pow(16, modifier))
            modifier -= 1
        return(sum)


# the argparser
class CLIArgParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--wast", type=str,
                            help="path to the wasm text file")
        parser.add_argument("--wasm", type=str, nargs='+',
                            help="path to the wasm object file")
        parser.add_argument("--asb", type=str,
                            help="path to the wast file to assemble")
        parser.add_argument("--dis", type=str,
                            help="path to the wasm file to disassemble")
        parser.add_argument("-o", type=str, help="the path to the output file")
        parser.add_argument("--dbg", action='store_true', help="print debug info", default=False)
        parser.add_argument("--unval", action='store_true', help="skips validation tests", default=False)
        parser.add_argument("--memdump", type=int, help="dumps the linear memory")
        parser.add_argument("--idxspc", action='store_true', help="print index space data", default=False)
        parser.add_argument("--run", action='store_true', help="runs the start function", default=False)
        parser.add_argument("--metric", action='store_true', help="print metrics", default=False)
        parser.add_argument("--gas", action='store_true', help="print gas usage", default=False)

        self.args = parser.parse_args()

        if self.args.wasm is not None and self.args.wast is not None:
            raise Exception("the --wast option and the --wasm option cannot\
                            be set at the same time. you need to choose one.")

    def getWASTPath(self):
        return self.args.wast

    def getWASMPath(self):
        return self.args.wasm

    def getASPath(self):
        return self.args.asb

    def getDISASPath(self):
        return self.args.dis

    def getOutputPath(self):
        return self.args.o

    def getDBG(self):
        return self.args.dbg

    def getUNVAL(self):
        return self.args.unval

    def getMEMDUMP(self):
        return self.args.memdump

    def getIDXSPC(self):
        return self.args.idxspc

    def getRun(self):
        return self.args.run

    def getMetric(self):
        return self.args.metric

    def getGas(self):
        return self.args.gas

    def getParseFlags(self):
        return(ParseFlags(self.args.wast, self.args.wasm, self.args.asb, self.args.dis,
                          self.args.o, self.args.dbg, self.args.unval, self.args.memdump,
                          self.args.idxspc, self.args.run, self.args.metric, self.args.gas))


# this class is responsible for reading the wasm text file- the first part of
# our assembler
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
            print(Colors.green + self.wast_header_type[element] + Colors.ENDC)

    def PrintImportDict(self):
        for element in self.wast_header_import:
            print(Colors.red + self.wast_header_import[element] + Colors.ENDC)

    def PrintTableDict(self):
        for element in self.wast_header_table:
            print(Colors.purple + self.wast_header_table[element] + Colors.ENDC)

    def PrintElemDict(self):
        for element in self.wast_header_elem:
            print(Colors.blue + self.wast_header_elem[element] + Colors.ENDC)

    def PrintMemoryDict(self):
        for element in self.wast_header_memory:
            print(Colors.darkgrey + self.wast_header_memory[element] +
                  Colors.ENDC)

    def PrintDataDict(self):
        for element in self.wast_header_data:
            print(Colors.yellow + self.wast_header_data[element] + Colors.ENDC)

    def PrintExportDict(self):
        for element in self.wast_header_export:
            print(Colors.cyan + self.wast_header_export[element] + Colors.ENDC)

    def PrintFuncDict(self):
        for element in self.wast_header_func:
            print(Colors.purple + self.wast_header_func[element] + Colors.ENDC)

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


# this class essentially holds our s-expr lexer. the current implementation
# only uses the lexer to read the function bodies.
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
            print(Colors.blue + self.wast_obj_func[funcbody] + Colors.ENDC)

            most_concat_sexpr = re.findall(sexpr_pattern,
                                           self.wast_obj_func[funcbody])
            print ('-----------------------------')

            for elem in most_concat_sexpr:
                print(elem)
                print ('-----------------------------')
                elem.split

    def ParseBodyV3(self, Print):
        stack = []
        expr = []
        full = []
        sexpr_greedy = re.compile('\s*(?:(?P<lparen>\()|(?P<rparen>\))|(?P<operandnum>[i|ui][0-9]+$)|(?P<regarg>\$[0-9]+$)|(?P<keyword>[a-zA-Z0-9\._]+)|(?P<identifier>[\$][a-zA-Z0-9_\$]+))')

        for funcbody in self.wast_obj_func:
            for stackval in re.finditer(sexpr_greedy,
                                        self.wast_obj_func[funcbody]):
                for k, v in stackval.groupdict().items():
                    if Print:
                        if v is not None:
                            print(k, v)

                    if v is not None:
                        if k == 'rparen':
                            flag = True
                            expr.append(v)
                            while flag:
                                temp = stack.pop()
                                if temp is '(':
                                    flag = False
                                expr.append(temp)
                            full.append(expr)
                            expr = []
                        else:
                            stack.append(v)

        for val in full:
            print(val)
        return(full)


# the code emitter for the assembler. incomplete.
class WASM_CodeEmitter(object):
    Obj_file = []
    Obj_Header = []
    little_endian = True

    def __init__(self, stack):
        self.stack = stack

    def SetNewStack(self, new_stack):
        self.stack = new_stack

    def Obj_Header_32(self):
        magic_number = '0061736d'
        version = '01000000'

        self.Obj_file.append(magic_number)
        self.Obj_file.append(version)

    def EmitTypeHeader(self):
        val_cnt = 0
        byte_cnt = 0
        word = str()
        param_sentence = str()
        result_sentence = str()
        tmp_obj = []

        for stacks in self.stack:
            for stack_value in stacks:
                if stack_value in WASM_OP_Code.type_ops_dict:
                    if stack_value == 'func':
                        tmp_obj.append(WASM_OP_Code.type_ops_dict[stack_value])
                        if param_sentence != "":
                            tmp_obj.append(param_sentence)
                        else:
                            tmp_obj.append("00")
                            byte_cnt += 1

                        if result_sentence != "":
                            tmp_obj.append(result_sentence)
                        else:
                            tmp_obj.append("00")
                            byte_cnt += 1

                        param_sentence = ""
                        result_sentence = ""
                        val_cnt = 0
                    else:
                        word += WASM_OP_Code.type_ops_dict[stack_value]
                        val_cnt += 1
                    byte_cnt += 1
                elif stack_value == 'param':
                    param_sentence += str(bytes([val_cnt])) + word
                    byte_cnt += 1
                    val_cnt = 0
                    word = ""
                elif stack_value == 'result':
                    result_sentence += str(bytes([val_cnt])) + word
                    byte_cnt += 1
                    val_cnt = 0
                    word = ""

        tmp_obj.insert(0, '8080')
        tmp_obj.insert(0, format(byte_cnt, 'x'))
        # tmp_obj.insert(0, WASM_OP_Code.section_code_dict['type'])
        tmp_obj.insert(0, "01")
        # tmp_obj.insert(0, '01')
        self.Obj_Header = tmp_obj

    def PrintTypeHeaderObj(self):
        # print(self.Obj_Header)

        for byte in self.Obj_Header:
            print(byte)

    def Dump_Obj_STDOUT(self):
        for bytecode in self.Obj_file:
            print(bytecode)


# reads a wasm-obj file, returns a parsedstruct that holds all the sections'
# bytecode, their section type and their length
def ReadWASM(file_path, endianness, is_extended_isa, dbg):
    temp_obj_file = []
    wasm_file = open(file_path, "rb")
    parsedstruct = ParsedStruct()
    # read the magic cookie
    byte = wasm_file.read(WASM_OP_Code.uint32)
    if byte != WASM_OP_Code.magic_number.to_bytes(
            WASM_OP_Code.uint32, byteorder=endianness, signed=False):
        raise Exception("bad magic cookie")

    # read the version number
    byte = wasm_file.read(WASM_OP_Code.uint32)
    if byte != WASM_OP_Code.version_number.to_bytes(
            WASM_OP_Code.uint32, byteorder=endianness, signed=False):
        raise Exception("bad version number")
    else:
        parsedstruct.version_number = byte

    while True:
        byte = wasm_file.read(1)
        if byte != b'':
            temp_obj_file.append(int.from_bytes(byte, byteorder='big', signed=False))
        else:
            break

    offset = 0
    loop = True
    while loop:
        try:
            section_id, offset, dummy = Read(temp_obj_file, offset, 'varuint7')
        except IndexError:
            break

        payload_length, offset, dummy = Read(temp_obj_file, offset, 'varuint32')

        if section_id == 0:
            is_custom_section = True
            name_len, offset, dummy = Read(temp_obj_file, offset, 'varuint32')
            name = temp_obj_file[offset : offset + name_len]
            offset += name_len
        else:
            is_custom_section = False
            name_len = 0
            name = ''
            dummy = 0

        payload_data = temp_obj_file[offset:offset + payload_length - name_len - dummy]
        offset += payload_length - name_len - dummy

        # @DEVI-the second field is for general use. it is unused right
        # now so we are filling it with jojo.
        parsedstruct.section_list.append([section_id, 'jojo',
                                            payload_length,
                                            is_custom_section,
                                            name_len, name,
                                            payload_data])

    # prints out the sections in the wasm object
    # for section in parsedstruct.section_list:
        # print(section)
    wasm_file.close()
    return(parsedstruct)


# Receives a parsedstruct returned from ReadWASM, parses all the sections and
# fills up a module class. the parse method, then can return the module.
# the returned class objects are all defined in section_structs.py.
class ObjReader(object):
    def __init__(self, parsedstruct):
        self.parsedstruct = parsedstruct

    # we use this method to read the operands of instructions. it's only
    # called by ReadCodeSection
    def Disassemble(self, section_byte, offset):
        matched = False
        read_bytes = 0
        read_bytes_temp = 0
        read_bytes_temp_iter = 0
        instruction = str()
        temp_wasm_ins = WASM_Ins()

        # @DEVI-FIXME-for v1.0 opcodes. needs to get fixed for extended
        # op-codes. ideally the mosule should hold its version number so we can
        # check it here.
        byte = format(section_byte[6][offset], '02x')
        offset += 1
        read_bytes += 1

        for op_code in WASM_OP_Code.all_ops:
            if op_code[1] == byte:
                matched = True

                # br_table has special immediates
                # @DEVI-FIXME-this is costing us quite dearly for every opcode
                # we read(at least two ticks per opcode). I could have the
                # br_table opcode done separately but kinda hurts the codes
                # uniformity. anyways.
                if op_code[1] == '0e':
                    matched = True
                    temp, offset, read_bytes_temp_iter = Read(
                        section_byte[6], offset, op_code[3][0])
                    instruction += repr(temp) + ' '
                    read_bytes_temp += read_bytes_temp_iter
                    for target_table in range(0, temp):
                        temp, offset, read_bytes_temp_iter = Read(section_byte[6], offset, op_code[3][1])
                        read_bytes_temp += read_bytes_temp_iter
                        instruction += repr(temp) + ' '
                    temp, offset, read_bytes_temp_iter = Read(
                        section_byte[6], offset, op_code[3][2])
                    instruction += repr(temp) + ' '
                    read_bytes_temp += read_bytes_temp_iter
                elif op_code[2]:
                    if isinstance(op_code[3], tuple):
                        for i in range(0, len(op_code [3])):
                            temp, offset, read_bytes_temp_iter = Read(
                                section_byte[6], offset, op_code[3][i])
                            read_bytes_temp += read_bytes_temp_iter
                            instruction += repr(temp) + ' '
                    else:
                        temp, offset, read_bytes_temp = Read(
                            section_byte[6], offset, op_code[3])
                        instruction += repr(temp)

                temp_wasm_ins.opcode = op_code[0]
                temp_wasm_ins.opcodeint = int(byte, 16)
                temp_wasm_ins.operands = instruction
                instruction = str()
                break

        read_bytes += read_bytes_temp
        return offset, matched, read_bytes, temp_wasm_ins

    # parses the code section. returns a Code_Section class
    def ReadCodeSection(self):
        offset = 0
        CS = Code_Section()
        temp_func_bodies = Func_Body()
        temp_local_entry = Local_Entry()
        section_exists = False
        for whatever in self.parsedstruct.section_list:
            # 10 is the code section
            if whatever[0] == 10:
                code_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        fn_cn, offset, dummy = Read(code_section[6], offset, 'varuint32')
        function_cnt = fn_cn
        CS.count = function_cnt

        while function_cnt > 0:
            function_body_length, offset, dummy = Read(code_section[6], offset, 'varuint32')
            temp_func_bodies.body_size = function_body_length

            local_count, offset, dummy = Read(code_section[6], offset, 'varuint32')
            temp_func_bodies.local_count = local_count

            # local_count_size will eventually hold how many bytes we will read
            # in total because of the local section
            local_count_size = dummy
            if local_count != 0:
                for i in range(0, local_count):
                    partial_local_count, offset, dummy = Read(code_section[6], offset, 'varuint32')
                    local_count_size += dummy
                    partial_local_type, offset, dummy = Read(code_section[6], offset, 'uint8')
                    local_count_size += dummy
                    temp_local_entry.count = partial_local_count
                    temp_local_entry.type = partial_local_type
                    temp_func_bodies.locals.append(deepcopy(temp_local_entry))
                    local_count -= partial_local_count
            else:
                pass

            read_bytes_so_far = local_count_size
            for i in range(0, function_body_length - local_count_size):
                offset, matched, read_bytes, temp_wasm_ins = self.Disassemble(
                    code_section, offset)
                temp_func_bodies.code.append(deepcopy(temp_wasm_ins))

                if not matched:
                    print(Colors.red + 'did not match anything' + Colors.ENDC)
                    print(Colors.red + 'code section offset: ' + repr(offset) + Colors.ENDC)
                    print(Colors.red + 'read bytes: ' + repr(read_bytes) + Colors.ENDC)
                    print(Colors.red + 'wasm ins: ' + repr(temp_wasm_ins.opcode) + Colors.ENDC)

                    for iter in temp_func_bodies.code:
                        print(iter.opcode)
                        print(iter.operands)
                    sys.exit(1)
                else:
                    pass
                matched = False
                read_bytes_so_far += read_bytes
                if read_bytes_so_far == function_body_length:
                    break

            CS.func_bodies.append(deepcopy(temp_func_bodies))
            temp_func_bodies.locals = []
            temp_func_bodies.code = []
            function_cnt -= 1
        return(CS)

    # parsed the data section. returns a Data_Section class
    def ReadDataSection(self):
        loop = True
        section_exists = False
        offset = 0
        DS = Data_Section()
        temp_data_segment = Data_Segment()
        init_expr = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 11:
                data_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        data_entry_count, offset, dummy = Read(data_section[6], offset, 'varuint32')
        DS.count = data_entry_count

        while data_entry_count != 0:
            linear_memory_index, offset, dummy = Read(data_section[6], offset, 'varuint32')
            temp_data_segment.index = linear_memory_index

            # reading in the init-expr
            while loop:
                # @DEVI-FIXME-this only works for none extended opcodes
                if data_section[6][offset] == 0x0b:
                    loop = False
                data_char, offset, dummy = Read(data_section[6], offset, 'uint8')
                init_expr.append(data_char)

            temp_data_segment.offset = init_expr

            data_entry_length, offset, dummy = Read(data_section[6], offset, 'varuint32')
            temp_data_segment.size = data_entry_length

            data_itself = data_section[6][offset:offset + data_entry_length]
            temp_data_segment.data = data_itself
            offset += data_entry_length

            DS.data_segments.append(deepcopy(temp_data_segment))

            data_entry_count -= 1
            init_expr = []
            loop = True
        return(DS)

    # parses the import section. returns an Import_Section class
    def ReadImportSection(self):
        offset = 0
        section_exists = False
        module_name = []
        field_name = []
        IS = Import_Section()
        temp_import_entry = Import_Entry()
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 2:
                import_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        import_cnt, offset, dummy = Read(import_section[6], offset, 'varuint32')
        IS.count = import_cnt

        while import_cnt != 0:
            module_length, offset, dummy = Read(import_section[6], offset, 'varuint32')
            temp_import_entry.module_len = module_length

            for i in range(0, module_length):
                module_name.append(import_section[6][offset + i])
            temp_import_entry.module_str = module_name
            offset += module_length

            field_length, offset, dummy = Read(import_section[6], offset, 'varuint32')
            temp_import_entry.field_len = field_length
            for i in range(0, field_length):
                field_name.append(import_section[6][offset + i])
            temp_import_entry.field_str = field_name
            offset += field_length

            kind, offset, dummy = Read(import_section[6], offset, 'uint8')
            temp_import_entry.kind = kind

            # function type
            if kind == 0:
                import_type, offset, dummy = Read(import_section[6], offset, 'varuint32')
                temp_import_entry.type = import_type
            # table type
            elif kind == 1:
                table_type = Table_Type()
                table_type.elemet_type, offset, dummy = Read(import_section[6], offset, 'varint7')
                rsz_limits = Resizable_Limits()
                rsz_limits.flags, offset, dummy = Read(import_section[6], offset, 'varuint1')
                rsz_limits.initial, offset, dummy = Read(import_section[6], offset, 'varuint32')
                if rsz_limits.flags:
                    rsz_limits.maximum, offset, dummy = Read(import_section[6], offset, 'varuint32')
                table_type.limit = rsz_limits
                temp_import_entry.type = table_type
            elif kind == 2:
                memory_type = Memory_Type()
                rsz_limits = Resizable_Limits()
                rsz_limits.flags, offset, dummy = Read(import_section[6], offset, 'varuint1')
                rsz_limits.initial, offset, dummy = Read(import_section[6], offset, 'varuint32')
                if rsz_limits.flags:
                    rsz_limits.maximum, offset, dummy = Read(import_section[6], offset, 'varuint32')
                memory_type.limits = rsz_limits
                temp_import_entry.type = memory_type
            elif kind == 3:
                global_type = Global_Type()
                global_type.content_type, offset, dummy = Read(import_section[6], offset, 'uint8')
                global_type.mutability, offset, dummy = Read(import_section[6], offset, 'varuint1')
                temp_import_entry.type = global_type

            IS.import_entry.append(deepcopy(temp_import_entry))

            import_cnt -= 1
            module_name = []
            field_name = []
        return(IS)

    # parses the export section, returns an Export_Section class
    def ReadExportSection(self):
        offset = 0
        section_exists = False
        field_name = []
        ES = Export_Section()
        temp_export_entry = Export_Entry()
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 7:
                export_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        export_entry_cnt, offset, dummy = Read(export_section[6], offset, 'varuint32')
        ES.count = export_entry_cnt

        while export_entry_cnt != 0:
            field_length, offset, dummy = Read(export_section[6], offset, 'varuint32')
            temp_export_entry.field_len = field_length

            for i in range(0, field_length):
                field_name.append(export_section[6][offset + i])
            temp_export_entry.fiels_str = field_name
            offset += field_length

            kind, offset, dummy = Read(export_section[6], offset, 'uint8')
            temp_export_entry.kind = kind

            index, offset, dummy = Read(export_section[6], offset, 'varuint32')
            temp_export_entry.index = index

            ES.export_entries.append(deepcopy(temp_export_entry))

            export_entry_cnt -= 1
            field_name = []
        return(ES)

    # parses the type section, returns a Type_Section class
    def ReadTypeSection(self):
        offset = 0
        section_exists = False
        param_list = []
        return_list = []
        TS = Type_Section()
        temp_func_type = Func_Type()
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 1:
                type_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        type_entry_count, offset, dummy = Read(type_section[6], offset, 'varuint32')
        TS.count = type_entry_count

        while type_entry_count != 0:
            form, offset, dummy = Read(type_section[6], offset, 'varint7')
            temp_func_type.form = form

            param_count, offset, dummy = Read(type_section[6], offset, 'varuint32')
            temp_func_type.param_cnt = param_count

            for i in range(0, param_count):
                param_list.append(type_section[6][offset + i])
            temp_func_type.param_types = param_list
            offset += param_count

            # @DEVI-FIXME- only works for MVP || single return value
            return_count, offset, dummy = Read(type_section[6], offset, 'varuint1')
            temp_func_type.return_cnt = return_count

            for i in range(0, return_count):
                return_list.append(type_section[6][offset + i])
            temp_func_type.return_type = return_list
            offset += return_count

            TS.func_types.append(deepcopy(temp_func_type))

            type_entry_count -= 1
            param_list = []
            return_list = []
        return(TS)

    # parses the function section, returns a Function_section class
    def ReadFunctionSection(self):
        offset = 0
        section_exists = False
        index_to_type = []
        FS = Function_Section()
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 3:
                function_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        function_entry_count, offset, dummy = Read(function_section[6], offset, 'varuint32')
        FS.count = function_entry_count

        for i in range(0, function_entry_count):
            index, offset, dummy = Read(function_section[6], offset, 'varuint32')
            index_to_type.append(index)
        FS.type_section_index = index_to_type
        offset += function_entry_count
        return(FS)

    # parses the element secction, returns an Element_Section class
    def ReadElementSection(self):
        offset = 0
        section_exists = False
        init_expr = []
        loop = True
        function_indices = []
        ES = Element_Section()
        temp_elem_segment = Elem_Segment()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 9:
                element_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        element_entry_count, offset, dummy = Read(element_section[6], offset, 'varuint32')
        ES.count = element_entry_count

        while element_entry_count != 0:
            table_index, offset, dummy = Read(element_section[6], offset, 'varuint32')
            temp_elem_segment.index = table_index

            # @DEVI-FIXME-only works for non-extneded opcodes
            while loop:
                if element_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(element_section[6][offset])
                offset += 1
            temp_elem_segment.offset = init_expr

            num_elements, offset, dummy = Read(element_section[6], offset, 'varuint32')
            temp_elem_segment.num_elem = num_elements

            for i in range(0, num_elements):
                index, offset, dummy = Read(element_section[6], offset, 'varuint32')
                function_indices.append(index)
            temp_elem_segment.elems = function_indices
            offset += num_elements

            ES.elem_segments.append(deepcopy(temp_elem_segment))

            loop = True
            init_expr = []
            function_indices = []
            element_entry_count -= 1
        return(ES)

    # parses the memory section, returns a Memory_Section class
    def ReadMemorySection(self):
        offset = 0
        section_exists = False
        MS = Memory_Section()
        temp_rsz_limits = Resizable_Limits()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 5:
                memory_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        num_linear_mems, offset, dummy = Read(memory_section[6], offset, 'varuint32')
        MS.count = num_linear_mems

        while num_linear_mems != 0:
            flag, offset, dummy = Read(memory_section[6], offset, 'varuint1')
            temp_rsz_limits.flags = flag

            initial,offset, dummy = Read(memory_section[6], offset, 'varuint32')
            temp_rsz_limits.initial = initial

            if flag:
                maximum, offset, dummy = Read(memory_section[6], offset, 'varuint32')
                temp_rsz_limits.maximum = maximum

            MS.memory_types.append(deepcopy(temp_rsz_limits))
            num_linear_mems -= 1
        return(MS)

    # parses the table section, returns a Table_Section class
    def ReadTableSection(self):
        offset = 0
        section_exists = False
        TS = Table_Section()
        temp_table_type = Table_Type()
        temp_rsz_limits = Resizable_Limits()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 4:
                table_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        table_count, offset, dummy = Read(table_section[6], offset, 'varuint32')
        TS.count = table_count

        while table_count != 0:
            element_type, offset, dummy = Read(table_section[6], offset, 'varint7')
            temp_table_type.element_type = element_type

            flag, offset, dummy = Read(table_section[6], offset, 'varuint1')
            temp_rsz_limits.flags = flag

            initial, offset, dummy = Read(table_section[6], offset, 'varuint32')
            temp_rsz_limits.initial = initial

            if flag:
                maximum, offset, dummy = Read(table_section[6], offset, 'varuint32')
                temp_rsz_limits.maximum = maximum

            temp_table_type.limit = temp_rsz_limits
            TS.table_types.append(deepcopy(temp_table_type))

            table_count -= 1
        return(TS)

    # parses the global section, returns a Global_Section class
    def ReadGlobalSection(self):
        offset = 0
        loop = True
        section_exists = False
        init_expr = []
        GS = Global_Section()
        temp_gl_var = Global_Variable()
        temp_gl_type = Global_Type()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 6:
                global_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        count, offset, dummy = Read(global_section[6], offset, 'varuint32')
        GS.count = count

        while count != 0:
            content_type, offset, dummy = Read(global_section[6], offset, 'uint8')
            temp_gl_type.content_type = content_type

            mutability, offset, dummy = Read(global_section[6], offset, 'varuint1')
            temp_gl_type.mutability = mutability

            # @DEVI-FIXME-only works for non-extended opcodes
            while loop:
                if global_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(global_section[6][offset])
                offset += 1
            temp_gl_var.init_expr = init_expr

            temp_gl_var.global_type = temp_gl_type
            GS.global_variables.append(deepcopy(temp_gl_var))


            count -= 1
            loop = True
            init_expr = []
        return(GS)

    # parses the start section, returns a Start_Section
    def ReadStartSection(self):
        offset = 0
        section_exists = False
        SS = Start_Section()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 8:
                start_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        function_index, offset, dummy = Read(start_section[6], offset, 'varuint32')
        SS.function_section_index = function_index
        return(SS)

    # unused-returns the cursor location in the object file
    def getCursorLocation(self):
        return(self.wasm_file.tell())

    # a convinience method-builds a module class and returns it
    def parse(self):
        return(Module(self.ReadTypeSection(), self.ReadImportSection(),
                      self.ReadFunctionSection(), self.ReadTableSection(),
                      self.ReadMemorySection(), self.ReadGlobalSection(),
                      self.ReadExportSection(), self.ReadStartSection(),
                      self.ReadElementSection(), self.ReadCodeSection(),
                      self.ReadDataSection()))


# WIP-basically how the assembler is constructed
class ParserV1(object):
    def __init__(self, path):
        self.path = path

    def run(self):
        wasmtobj = WASMText(self.path)
        # wasmtobj.test_print()
        wasmtobj.RegExSearch()
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
        wasmtobj.FuncParserTest()

        funcbodyparser = FuncBodyParser(wasmtobj.getFuncBodies())
        headerparser = FuncBodyParser(wasmtobj.getTypeHeader())

        expr_stack = funcbodyparser.ParseBodyV3(False)
        header_stack = headerparser.ParseBodyV3(True)

        wasm_codeemitter = WASM_CodeEmitter(expr_stack)
        wasm_codeemitter.Obj_Header_32()
        wasm_codeemitter.Dump_Obj_STDOUT()

        wasm_codeemitter.SetNewStack(header_stack)
        wasm_codeemitter.EmitTypeHeader()
        wasm_codeemitter.PrintTypeHeaderObj()


# our interpreter class
class PythonInterpreter(object):
    def __init__(self):
        self.modules = []

    # appends a module to the module list that PythonInterpreter has
    def appendmodule(self, module):
        self.modules.append(module)

    # returns the list of modules that we have parsed so far
    def getmodules(self):
        return(self.modules)

    # convinience method.calls the ObjReader to parse a wasm obj file.
    # returns a module class.
    def parse(self, file_path):
        parser = ObjReader(ReadWASM(file_path, 'little', False, True))
        return(parser.parse())

    # dumps the object sections' info to stdout. pretty print.
    def dump_sections(self, module):
        print(Colors.blue + Colors.BOLD +
                'BEGENNING OF MODULE' + Colors.ENDC)

        # type_section
        if module.type_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Type Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.type_section.count))
            for iter in module.type_section.func_types:
                print(Colors.cyan + 'form: ' + repr(iter.form) + Colors.ENDC)
                print(Colors.green + 'param count: ' + repr(iter.param_cnt) + Colors.ENDC)
                print(Colors.red + 'param types: ' + repr(iter.param_types) + Colors.ENDC)
                print(Colors.purple + 'return count: ' + repr(iter.return_cnt) + Colors.ENDC)
                print(Colors.yellow + 'return type: ' + repr(iter.return_type) + Colors.ENDC)

        # import_section
        if module.import_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Import Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.import_section.count))
            for iter in module.import_section.import_entry:
                print(Colors.cyan + 'module length: ' + repr(iter.module_len) + Colors.ENDC)
                print(Colors.green + 'module str: ' + repr(iter.module_str) + Colors.ENDC)
                print(Colors.red + 'field length: ' + repr(iter.field_len) + Colors.ENDC)
                print(Colors.purple + 'field str: ' + repr(iter.field_str) + Colors.ENDC)
                print(Colors.yellow + 'kind: ' + repr(iter.kind) + Colors.ENDC)
                print(Colors.grey + 'type: ' + repr(iter.type) + Colors.ENDC)

        # function_section
        if module.function_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Function Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.function_section.count))
            for iter in module.function_section.type_section_index:
                print(Colors.cyan + 'type section index: ' + repr(iter) + Colors.ENDC)

        # table_section
        if module.table_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Table Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.table_section.count))
            for iter in module.table_section.table_types:
                print(Colors.cyan + 'element type: ' + repr(iter.element_type) + Colors.ENDC)
                print(Colors.green + 'Resizable_Limits:flags: ' + repr(iter.limit.flags) + Colors.ENDC)
                print(Colors.red + 'Resizable_Limits:initial: ' + repr(iter.limit.initial) + Colors.ENDC)
                print(Colors.purple + 'Resizable_Limits:maximum: ' + repr(iter.limit.maximum) + Colors.ENDC)

        # memory_section
        if module.memory_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Memory Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.memory_section.count))
            for iter in module.memory_section.memory_types:
                print(Colors.green + 'Resizable_Limits:flags: ' + repr(iter.flags) + Colors.ENDC)
                print(Colors.red + 'Resizable_Limits:initial: ' + repr(iter.initial) + Colors.ENDC)
                print(Colors.purple + 'Resizable_Limits:maximum: ' + repr(iter.maximum) + Colors.ENDC)

        # global_section
        if module.global_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Global Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.global_section.count))
            for iter in module.global_section.global_variables:
                print(Colors.green + 'global type: ' + repr(iter.global_type) + Colors.ENDC)
                print(Colors.red + 'init expr: ' + repr(iter.init_expr) + Colors.ENDC)

        # export_section
        if module.export_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Export Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.export_section.count))
            for iter in module.export_section.export_entries:
                print(Colors.green + 'field length: ' + repr(iter.field_len) + Colors.ENDC)
                print(Colors.red + 'field str: ' + repr(iter.field_str) + Colors.ENDC)
                print(Colors.purple + 'kind: ' + repr(iter.kind) + Colors.ENDC)
                print(Colors.cyan + 'index: ' + repr(iter.index) + Colors.ENDC)

        # start_section
        if module.start_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Start Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('start function index: ' + repr(module.start_section.function_section_index))

        # element_section
        if module.element_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Element Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.element_section.count))
            for iter in module.element_section.elem_segments:
                print(Colors.green + 'index: ' + repr(iter.index) + Colors.ENDC)
                print(Colors.red + 'offset: ' + repr(iter.offset) + Colors.ENDC)
                print(Colors.purple + 'num_elem: ' + repr(iter.num_elem) + Colors.ENDC)
                print(Colors.cyan + 'elemes:' + repr(iter.elems) + Colors.ENDC)

        # code_section
        if module.code_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Code Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.code_section.count))
            for iter in module.code_section.func_bodies:
                print(Colors.green + 'body size: ' + repr(iter.body_size) + Colors.ENDC)
                print(Colors.red + 'local enrty count: ' + repr(iter.local_count) + Colors.ENDC)
                for iterer in iter.locals:
                    print(Colors.blue + 'local count: ' + repr(iterer.count) + Colors.ENDC)
                    print(Colors.blue + 'local type: ' + repr(iterer.type) + Colors.ENDC)
                for iterer in iter.code:
                    instruction = iterer.opcode + ' ' + iterer.operands
                    print(Colors.cyan + 'opcode: ' + repr(iterer.opcode) + Colors.ENDC)
                    print(Colors.grey + 'immediate: ' + repr(iterer.operands) + Colors.ENDC)
                    print(Colors.yellow + instruction + Colors.ENDC)

        # data_section
        if module.data_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + Colors.BOLD + 'Data Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.data_section.count))
            for iter in module.data_section.data_segments:
                print(Colors.green + 'index: ' + repr(iter.index) + Colors.ENDC)
                print(Colors.red + 'offset: ' + repr(iter.offset) + Colors.ENDC)
                print(Colors.purple + 'size: ' + repr(iter.size) + Colors.ENDC)
                print(Colors.cyan + 'data:' + repr(iter.data) + Colors.ENDC)

    # palceholder for the validation tests
    def runValidations(self):
        modulevalidation = ModuleValidation(self.modules[0])
        return(modulevalidation.ValidateAll())



def main():
    argparser = CLIArgParser()

    # this is essentially how we use our current interpreter. it reads in wasm
    # obj files and holds keeps the parses modules. Theb we run the validation
    # tests and initialize the WASM machine
    if argparser.getWASMPath() is not None:
        interpreter = PythonInterpreter()
        for file_path in argparser.getWASMPath():
            module = interpreter.parse(file_path)
            interpreter.appendmodule(module)
            if argparser.getDBG():
                interpreter.dump_sections(module)
            if interpreter.runValidations():
                #run the interpreter
                pass
            else:
                print(Colors.red + 'failed validation tests' + Colors.ENDC)
            vm = VM(interpreter.getmodules())
            vm.setFlags(argparser.getParseFlags())
            ms = vm.getState()
            if argparser.getIDXSPC():
                DumpIndexSpaces(ms)
            if argparser.getMEMDUMP():
                DumpLinearMems(ms.Linear_Memory, argparser.getMEMDUMP())
            if argparser.getRun():
                vm.run()
            # merklizer = Merklizer(ms.Linear_Memory[0][0:512], module)
            # treelength, hashtree = merklizer.run()


    if argparser.getWASTPath() is not None:
        print(argparser.getWASTPath())
        parser = ParserV1(argparser.getWASTPath())
        parser.run()

    # WIP-the assmebler
    if argparser.getASPath() is not None:
        print("not implemented yet")
        sys.exit(1)

    # WIP-the disassmebler
    if argparser.getDISASPath() is not None:
        print("not implemented yet")
        sys.exit(1)


if __name__ == '__main__':
    main()
