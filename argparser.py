from __future__ import print_function
import argparse
import sys
import re
from utils import *
from OpCodes import *

_DBG_ = True


class ParsedSection(object):
    def __init__(self, section_id, section_name,
                 payload_length, is_custom_section,
                 name_len, name, payload_data):
        self.section_id = section_id
        self.section_name = section_name
        self.payload_length = payload_length
        self.is_custom_section = is_custom_section
        self.name_len = name_len
        self.name = name
        self.payload_data = payload_data

        if not isinstance(self.section_id, int):
            raise Exception("section_id must be an int")
        if not isinstance(self.section_name, str):
            raise Exception("section_name must be a str")
        if not isinstance(self.payload_length, int):
            raise Exception("payload_length must be an int")
        if not isinstance(self.is_custom_section, bool):
            raise Exception("is_custom_section must be a bool")
        if not isinstance(self.name_len, int):
            raise Exception("name_len must be an int")
        if not isinstance(self.name, bytearray):
            raise Exception("name must be a bytearray")
        if not isinstance(self.payload_data, bytearray):
            raise Exception("payload_data must be a bytearray")


class ParsedStruct:
    version_number = int()
    section_list = []


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


def ReadLEB128OperandsU(section_byte, offset, operand_count):
    seen_padding = False
    byte_count = 0
    operand = []
    return_list = []
    read_bytes = 0
    for i in range(0, operand_count):
        while True:
            # print(Colors.red + repr(section_byte) + Colors.ENDC)
            byte = int(section_byte[6][offset])
            byte_count += 1
            read_bytes += 1
            offset += 1
            if not seen_padding:
                operand.append(byte)

                if byte == 0x80:
                    # we have seen a padding byte so we should read 4 bytes in
                    # total
                    seen_padding = True
                elif byte & 0x80 != 0:
                    # we havent reached the last byre of the operand yet
                    pass
                else:
                    # we are reading the last byte of the operand
                    break

            if seen_padding:
                # if seen_padding:
                if seen_padding and byte_count == 4:
                    break
                elif seen_padding and not byte_count == 4:
                    operand.append(byte)

        seen_padding = False
        byte_count = 0
        return_list.append(operand)
        operand = []
    return return_list, offset, read_bytes


def ReadLEB128OperandsS(section_byte, offset, operand_count):
    pass


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
        parser.add_argument("-dbg", type=bool, help="print debug info")

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


# i know the name is off-putting but this is technically our lexer.
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


class ObjReader(object):
    parsedstruct = ParsedStruct

    def __init__(self, file_path, endianness, is_extended_isa, dbg):
        self.wasm_file = open(file_path, "rb")
        self.file_path = file_path
        self.endianness = endianness
        self.is_extended_isa = is_extended_isa
        self.dbg = dbg

    def testprintall(self):
        for line in self.wasm_file:
            print(line)
        self.wasm_file.seek(0)

    def testprintbyteall(self):
        byte = self.wasm_file.read(1)
        print(byte)
        while byte != b"":
            byte = self.wasm_file.read(1)
            print(byte)
        self.wasm_file.seek(0)

    def ReadWASM(self):
        # read the magic cookie
        byte = self.wasm_file.read(WASM_OP_Code.uint32)
        if byte != WASM_OP_Code.magic_number.to_bytes(
                WASM_OP_Code.uint32, byteorder=self.endianness, signed=False):
            raise Exception("bad magic cookie")

        # read the version number
        byte = self.wasm_file.read(WASM_OP_Code.uint32)
        if byte != WASM_OP_Code.version_number.to_bytes(
                WASM_OP_Code.uint32, byteorder=self.endianness, signed=False):
            raise Exception("bad version number")
        else:
            self.parsedstruct.version_number = byte

        while self.ReadSection():
            pass

    def ReadSection(self):
        section_id_int = int()
        payload_length_int = int()
        name_len_int = int()
        name = str()
        payload_data = bytearray()
        is_custom_section = False
        not_end_of_the_line = True
        section_id = self.wasm_file.read(WASM_OP_Code.varuint7)

        if section_id == b"":
            not_end_of_the_line = False
        else:
            section_id_int = LEB128UnsignedDecode(section_id)

            payload_length = self.wasm_file.read(WASM_OP_Code.varuint32)
            payload_length_int = LEB128UnsignedDecode(payload_length) + 1
            # print(payload_length_int)

            if section_id is not WASM_OP_Code.section_code_dict['custom']:
                payload_data = self.wasm_file.read(payload_length_int)
                # print(payload_data)
            else:
                is_custom_section = True
                name_len = self.wasm_file.read(WASM_OP_Code.varuint32)
                name_len_int = Conver2Int(self.endianness,
                                          WASM_OP_Code.varuint32,
                                          name_len)
                # print(name_len)
                name = self.wasm_file.read(name_len)
                payload_data = self.wasm_file.read(
                    payload_length_int - name_len_int - WASM_OP_Code.varuint32)

        self.parsedstruct.section_list.append([section_id_int, 'jojo',
                                               payload_length_int,
                                               is_custom_section,
                                               name_len_int, name,
                                               payload_data])

        return(not_end_of_the_line)

    def PrintAllSection(self):
        for section in self.parsedstruct.section_list:
            print(section)

    def DisassembleDebug(self, byte, offset):
        matched = False
        if WASM_OP_Code.control_flow_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.control_flow_ops_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.type_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.type_ops_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.num_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.num_ops_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.call_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.call_ops_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.mem_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.mem_ops_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.consts_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.consts_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.conversion_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.conversion_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.var_access_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.var_access_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.var_access_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.var_access_dict_rev[byte] + Colors.ENDC)
            matched = True
        elif WASM_OP_Code.param_ops_dict_rev.get(byte):
            print(Colors.green +
                  WASM_OP_Code.param_ops_dict_rev[byte] + Colors.ENDC)
            matched = True

        offset += 1
        return offset, matched

    def Disassemble(self, section_byte, offset):
        matched = False
        read_bytes = 0
        read_bytes_temp = 0
        instruction = str()
        print('offset = ' + repr(offset))
        byte = format(section_byte[6][offset], '02x')
        print(Colors.blue + repr(byte) + Colors.ENDC)
        offset += 1
        read_bytes += 1
        for op_code in WASM_OP_Code.all_ops:
            if op_code[1] == byte:
                matched = True

                if op_code[2]:
                    print(op_code[2])
                    print(op_code[3])
                    if isinstance(op_code[3], tuple):
                        temp, offset, read_bytes_temp = ReadLEB128OperandsU(
                            section_byte, offset, len(op_code[3]))
                        print('temp:' + repr(temp))
                        for i in range(0, len(op_code[3])):
                            instruction += repr(temp[i]) + ' '
                    else:
                        temp, offset, read_bytes_temp = ReadLEB128OperandsU(
                            section_byte, offset, 1)
                        print('temp:' + repr(temp))

                print(Colors.green +
                      op_code[0] + ' ' + instruction + Colors.ENDC)
                instruction = str()
                break

        read_bytes += read_bytes_temp
        print('read bytes this iteration:' + repr(read_bytes))
        return offset, matched, read_bytes

    def ReadCodeSection(self):
        offset = 1
        section_exists = False
        for whatever in self.parsedstruct.section_list:
            # 10 is the code section
            if whatever[0] == 10:
                code_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'code section:' + Colors.ENDC)
        print(code_section)
        print()

        function_cnt = code_section[6][offset]
        offset += 1
        print('function count :' + repr(function_cnt))

        while function_cnt > 0:
            print(code_section[6][offset:offset + 4])
            function_body_length = LEB128UnsignedDecode(
                code_section[6][offset:offset + 4])
            offset += 4
            print('function body length :' + repr(function_body_length))

            # yolo
            offset += 1

            local_count = Conver2Int(True, 1,
                                     code_section[6][offset:offset + 1])
            print(code_section[6][offset:offset + 1])
            offset += 1
            print('local count :' + repr(local_count))

            local_count_size = 1 + local_count
            if local_count != 0:
                for i in range(0, local_count):
                    partial_local_count = Conver2Int(
                        True, 1, code_section[6][offset:offset + 1])
                    offset += 1
                    print(Colors.purple +
                          repr(partial_local_count) + Colors.ENDC)
                    offset += 1
                    local_count -= partial_local_count
                    local_count_size += 1
            else:
                pass

            read_bytes_so_far = local_count_size
            print(Colors.purple + repr(local_count_size) + Colors.ENDC)
            for i in range(0, function_body_length - local_count_size):
                print('----------------------------------------')

                offset, matched, read_bytes = self.Disassemble(
                    code_section, offset)

                if not matched:
                    print(Colors.red + 'did not match anything' + Colors.ENDC)
                else:
                    print(Colors.yellow + 'matched something' + Colors.ENDC)
                matched = False
                read_bytes_so_far += read_bytes
                if read_bytes_so_far == function_body_length:
                    break

            function_cnt -= 1

    def ReadDataSection(self):
        loop = True
        section_exists = False
        offset = 1
        init_expr = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 11:
                data_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print(Colors.purple + 'data section:' + Colors.ENDC)
        print(data_section)
        print('')
        data_entry_count = data_section[6][offset]
        print(Colors.purple +
              'data entry count:' + repr(data_entry_count) + Colors.ENDC)
        offset += 1

        while data_entry_count != 0:
            linear_memory_index = data_section[6][offset]
            print(Colors.cyan +
                  'linear memory index:' +
                  repr(linear_memory_index) + Colors.ENDC)
            offset += 1

            while loop:
                if data_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(data_section[6][offset])
                offset += 1

            print(Colors.red +
                  'init expression:' + repr(init_expr) + Colors.ENDC)

            data_entry_length = data_section[6][offset]
            offset += 1
            print(Colors.blue +
                  'data entry length:' + repr(data_entry_length) + Colors.ENDC)

            data_itself = data_section[6][offset:offset + data_entry_length]
            print(Colors.green +
                  'data itslef:' + repr(data_itself) + Colors.ENDC)
            offset += data_entry_length

            print(Colors.yellow +
                  '-------------------------------------------------------'
                  + Colors.ENDC)
            data_entry_count -= 1
            init_expr = []
            loop = True

    def ReadImportSection(self):
        offset = 1
        section_exists = False
        module_name = []
        field_name = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 2:
                import_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print(Colors.purple + 'import section:' + Colors.ENDC)
        print(import_section)
        print()

        import_cnt = import_section[6][offset]
        print(Colors.purple + 'import count:' + repr(import_cnt) + Colors.ENDC)
        offset += 1

        while import_cnt != 0:
            module_length = import_section[6][offset]
            offset += 1
            print(Colors.blue +
                  'module length:' + repr(module_length) + Colors.ENDC)

            for i in range(0, module_length):
                module_name.append(import_section[6][offset + i])
            print(Colors.cyan
                  + 'module name:' + repr(module_name) + Colors.ENDC)
            offset += module_length

            field_length = import_section[6][offset]
            offset += 1
            print(Colors.grey
                  + 'field length:' + repr(field_length) + Colors.ENDC)
            for i in range(0, field_length):
                field_name.append(import_section[6][offset + i])
            print(Colors.red + 'field name:' + repr(field_name) + Colors.ENDC)
            offset += field_length

            kind = import_section[6][offset]
            print(Colors.purple + 'kind:' + repr(kind) + Colors.ENDC)
            offset += 1

            yolo_byte = import_section[6][offset:offset + 1]
            offset += 1
            print(Colors.yellow + 'yolo bytes:' + repr(yolo_byte) + Colors.ENDC)

            print(Colors.yellow +
                  '-------------------------------------------------------'
                  + Colors.ENDC)
            import_cnt -= 1
            module_name = []
            field_name = []

    def ReadSectionExport(self):
        offset = 1
        section_exists = False
        field_name = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 7:
                export_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print(Colors.purple + 'export section:' + Colors.ENDC)
        print(export_section)
        print()

        export_entry_cnt = export_section[6][offset]
        offset += 1
        print(Colors.purple
              + 'export entry count:' + repr(export_entry_cnt) + Colors.ENDC)

        while export_entry_cnt != 0:
            field_length = export_section[6][offset]
            offset += 1
            print(Colors.blue
                  + 'field_length:' + repr(field_length) + Colors.ENDC)

            for i in range(0, field_length):
                field_name.append(export_section[6][offset + i])
            offset += field_length
            print(Colors.cyan + 'field name:' + repr(field_name) + Colors.ENDC)

            kind = export_section[6][offset]
            offset += 1
            print(Colors.red + 'kind:' + repr(kind) + Colors.ENDC)

            index = export_section[6][offset]
            offset += 1
            print(Colors.grey + 'index:' + repr(index) + Colors.ENDC)

            print(Colors.green +
                  '-------------------------------------------------------'
                  + Colors.ENDC)
            export_entry_cnt -= 1
            field_name = []

    def ReadSectionType(self):
        offset = 1
        section_exists = False
        param_list = []
        return_list = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 1:
                type_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print(Colors.purple + 'type section:' + Colors.ENDC)
        print(type_section)
        print()

        type_entry_count = type_section[6][offset]
        offset += 1
        print(Colors.purple +
              'type section entry count:'
              + repr(type_entry_count) + Colors.ENDC)

        while type_entry_count != 0:
            form = type_section[6][offset]
            offset += 1
            print(Colors.grey + 'form:' + repr(form) + Colors.grey)
            param_count = type_section[6][offset]
            offset += 1
            print(Colors.blue +
                  'param count:' + repr(param_count) + Colors.ENDC)

            for i in range(0, param_count):
                param_list.append(type_section[6][offset + i])
            offset += param_count
            print(Colors.red + 'param list:' + repr(param_list) + Colors.ENDC)

            return_count = type_section[6][offset]
            offset += 1
            print(Colors.cyan +
                  'return count:' + repr(return_count) + Colors.ENDC)

            for i in range(0, return_count):
                return_list.append(type_section[6][offset + i])
            offset += return_count
            print(Colors.yellow +
                  'return list:' + repr(return_list) + Colors.ENDC)

            print(Colors.green +
                  '-------------------------------------------------------'
                  + Colors.ENDC)
            type_entry_count -= 1
            param_list = []
            return_list = []

    def ReadSectionFunction(self):
        offset = 1
        section_exists = False
        index_to_type = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 3:
                function_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'function section:' + Colors.ENDC)
        print(function_section)
        print()

        function_entry_count = function_section[6][offset]
        offset += 1
        print(Colors.purple +
              'function entry count:' +
              repr(function_entry_count) + Colors.ENDC)

        for i in range(0, function_entry_count):
            index_to_type.append(function_section[6][offset + i])
        offset += function_entry_count
        print(Colors.red +
              'indices into type section:' +
              repr(index_to_type) + Colors.ENDC)

    def ReadSectionElement(self):
        offset = 1
        section_exists = False
        init_expr = []
        loop = True
        function_indices = []

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 9:
                element_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'element section:' + Colors.ENDC)
        print(element_section)
        print()

        element_entry_count = element_section[6][offset]
        offset += 1
        print(Colors.purple +
              'entry count:' + repr(element_entry_count) + Colors.ENDC)

        while element_entry_count != 0:
            table_index = element_section[6][offset]
            offset += 1
            print(Colors.green +
                  'table index:' + repr(table_index) + Colors.ENDC)

            while loop:
                if element_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(element_section[6][offset])
                offset += 1

            print(Colors.red + 'init expr:' + repr(init_expr) + Colors.ENDC)

            num_elements = element_section[6][offset]
            print(Colors.cyan +
                  'number of elements:' + repr(num_elements) + Colors.ENDC)

            for i in range(0, num_elements):
                function_indices.append(element_section[6][offset + i])
            offset += num_elements
            print(Colors.grey +
                  'function indices:' + repr(function_indices) + Colors.ENDC)

            loop = True
            init_expr = []
            function_indices = []
            element_entry_count -= 1

    def ReadMemorySection(self):
        offset = 1
        section_exists = False

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 5:
                memory_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'memory section:' + Colors.ENDC)
        print(memory_section)
        print()

        num_linear_mems = memory_section[6][offset]
        offset += 1
        print(Colors.purple
              + 'num_linear_mems:' + repr(num_linear_mems) + Colors.ENDC)

        while num_linear_mems != 0:
            flag = memory_section[6][offset]
            offset += 1
            print(Colors.grey + 'flag:' + repr(flag) + Colors.ENDC)

            initial = LEB128UnsignedDecode(memory_section[6][offset:offset + 2])
            offset += 2
            print(Colors.green + 'initial size:' + repr(initial) + Colors.ENDC)

            if flag == 1:
                maximum = LEB128UnsignedDecode(
                    memory_section[6][offset:offset + 2])
                offset += 2
                print(Colors.blue + 'maximum:' + repr(maximum) + Colors.ENDC)

            num_linear_mems -= 1

    def ReadSectionTable(self):
        offset = 1
        section_exists = False

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 4:
                table_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'table section:' + Colors.ENDC)
        print(table_section)
        print()

        table_count = table_section[6][offset]
        offset += 1
        print(Colors.purple + 'table count:' + repr(table_count) + Colors.ENDC)

        while table_count != 0:
            element_type = table_section[6][offset]
            offset += 1
            print(Colors.cyan +
                  'element type:' + repr(element_type) + Colors.ENDC)

            flag = table_section[6][offset]
            offset += 1
            print(Colors.yellow + 'flag:' + repr(flag) + Colors.ENDC)

            initial = LEB128UnsignedDecode(table_section[6][offset:offset + 2])
            offset += 2
            print(Colors.green + 'initial size:' + repr(initial) + Colors.ENDC)

            if flag == 1:
                maximum = LEB128UnsignedDecode(
                    table_section[6][offset:offset + 2])
                offset += 2
                print(Colors.blue + 'maximum:' + repr(maximum) + Colors.ENDC)

            table_count -= 1

    def ReadSectionGlobal(self):
        offset = 1
        loop = True
        section_exists = False
        init_expr = []

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 6:
                global_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'global section:' + Colors.ENDC)
        print(global_section)
        print()

        count = global_section[6][offset]
        offset += 1
        print(Colors.purple + 'count:' + repr(count) + Colors.ENDC)

        while count != 0:
            content_type = global_section[6][offset]
            offset += 1
            print(Colors.cyan + repr(content_type) + Colors.ENDC)

            mutability = global_section[6][offset]
            offset += 1
            print(Colors.blue + repr(mutability) + Colors.ENDC)

            while loop:
                if global_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(global_section[6][offset])
                offset += 1

            print(Colors.red + repr(init_expr) + Colors.ENDC)

            count -= 1
            loop = True
            init_expr = []

    def ReadStartSection(self):
        offset = 1
        section_exists = False

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 8:
                start_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None
        print()
        print(Colors.purple + 'start section:' + Colors.ENDC)
        print(start_section)
        print()

        function_index = start_section[6][offset]
        offset += 1
        print(Colors.blue +
              'function index:' + repr(function_index) + Colors.ENDC)

    def getCursorLocation(self):
        return(self.wasm_file.tell())


class ParserV1(object):
    def run(self):
        argparser = CLIArgParser()
        wasmtobj = WASMText(argparser.getWASTPath())
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
        headerparser = FuncBodyParser(wasmtobj.getTypeHeader())

        expr_stack = funcbodyparser.ParseBodyV3(False)
        header_stack = headerparser.ParseBodyV3(True)

        wasm_codeemitter = WASM_CodeEmitter(expr_stack)
        wasm_codeemitter.Obj_Header_32()
        wasm_codeemitter.Dump_Obj_STDOUT()

        wasm_codeemitter.SetNewStack(header_stack)
        wasm_codeemitter.EmitTypeHeader()
        wasm_codeemitter.PrintTypeHeaderObj()


class PythonInterpreter(object):
    def run(self):
        argparser = CLIArgParser()
        for obj_file in argparser.getWASMPath():
            wasmobj = ObjReader(obj_file, 'little', False, True)
            # wasmobj.testprintall()
            # wasmobj.testprintbyteall()
            wasmobj.ReadWASM()
            # wasmobj.PrintAllSection()
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


def main():
    argparser = CLIArgParser()

    if argparser.getWASMPath() is not None:
        print(argparser.getWASMPath())
        parser = PythonInterpreter()
        parser.run()

    if argparser.getWASTPath() is not None:
        print(argparser.getWASTPath())
        parser = ParserV1()
        parser.run()

    if argparser.getASPath() is not None:
        print("not implemented yet")

    if argparser.getDISASPath() is not None:
        print("not implemented yet")


if __name__ == '__main__':
    main()
