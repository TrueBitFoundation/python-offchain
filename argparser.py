from __future__ import print_function
import argparse
import sys
import re
from section_structs import *
from utils import *
from OpCodes import *
from copy import deepcopy

_DBG_ = True


class ParsedStruct:
    def __init__(self):
        self.version_number = int()
        self.section_list = []


class ParsedStructV2:
    def __init__(self, version_number, section_list):
        self.version_number = version_number
        self.section_list = section_list


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


def Read(section_byte, offset, kind):
    seen_padding = False
    byte_count = 0
    operand = []
    return_list = []
    read_bytes = 0
    if kind == 'varuint1' or kind == 'varuint7' or kind == 'varuint32' or kind == 'varuint64' or kind == 'varint1' or kind == 'varint7' or kind == 'varint32' or kind == 'varint64':
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
                if seen_padding and byte_count == TypeDic[kind]:
                    break
                elif seen_padding and not byte_count == TypeDic[kind]:
                    operand.append(byte)

        seen_padding = False
        return_list.append(operand)
        operand = []
    elif kind == 'uint8' or kind == 'uint16' or kind == 'uint32' or kind == 'uint64':
        byte = section_byte[6][offset: offset + TypeDic[kind]]
        read_bytes += TypeDic[kind]
        offset += TypeDic[kind]
        operand.append(byte)
        return_list.append(operand)
        operand = []

    return return_list, offset, read_bytes


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


def ReadWASM(file_path, endianness, is_extended_isa, dbg):
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

    not_end_of_the_line = True
    while not_end_of_the_line:
        pass
        section_id_int = int()
        payload_length_int = int()
        name_len_int = int()
        name = str()
        payload_data = bytearray()
        is_custom_section = False
        section_id = wasm_file.read(WASM_OP_Code.varuint7)

        if section_id == b"":
            not_end_of_the_line = False
        else:
            section_id_int = LEB128UnsignedDecode(section_id)

            payload_length = wasm_file.read(WASM_OP_Code.varuint32)
            payload_length_int = LEB128UnsignedDecode(payload_length) + 1

            if section_id is not WASM_OP_Code.section_code_dict['custom']:
                payload_data = wasm_file.read(payload_length_int)
            else:
                is_custom_section = True
                name_len = wasm_file.read(WASM_OP_Code.varuint32)
                name_len_int = Conver2Int(endianness,
                                        WASM_OP_Code.varuint32,
                                        name_len)
                name = wasm_file.read(name_len)
                payload_data = wasm_file.read(
                    payload_length_int - name_len_int - WASM_OP_Code.varuint32)

        parsedstruct.section_list.append([section_id_int, 'jojo',
                                            payload_length_int,
                                            is_custom_section,
                                            name_len_int, name,
                                            payload_data])

    # for section in parsedstruct.section_list:
        # print(section)
    wasm_file.close()
    return(parsedstruct)


class ObjReader(object):
    def __init__(self, parsedstruct):
        self.parsedstruct = parsedstruct

    def Disassemble(self, section_byte, offset):
        matched = False
        read_bytes = 0
        read_bytes_temp = 0
        read_bytes_temp_iter = 0
        instruction = str()
        temp_wasm_ins = WASM_Ins()
        byte = format(section_byte[6][offset], '02x')
        offset += 1
        read_bytes += 1
        for op_code in WASM_OP_Code.all_ops:
            if op_code[1] == byte:
                matched = True

                if op_code[2]:
                    if isinstance(op_code[3], tuple):
                        for i in range(0, len(op_code [3])):
                            temp, offset, read_bytes_temp_iter = Read(
                                section_byte, offset, op_code[3][i])
                            read_bytes_temp += read_bytes_temp_iter
                            instruction += repr(temp) + ' '
                    else:
                        temp, offset, read_bytes_temp = Read(
                            section_byte, offset, op_code[3])
                        instruction += repr(temp)

                temp_wasm_ins.opcode = op_code[0]
                temp_wasm_ins.operands = instruction
                instruction = str()
                break

        read_bytes += read_bytes_temp
        return offset, matched, read_bytes, temp_wasm_ins

    def ReadCodeSection(self):
        offset = 1
        CS = Code_Section()
        temp_func_bodies = Func_Body()
        section_exists = False
        for whatever in self.parsedstruct.section_list:
            # 10 is the code section
            if whatever[0] == 10:
                code_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        function_cnt = code_section[6][offset]
        CS.count.append(function_cnt)
        offset += 1

        while function_cnt > 0:
            function_body_length = LEB128UnsignedDecode(
                code_section[6][offset:offset + 4])
            temp_func_bodies.body_size = function_body_length
            offset += 4

            # yolo
            offset += 1

            local_count = Conver2Int(True, 1,
                                     code_section[6][offset:offset + 1])
            temp_func_bodies.local_count = local_count
            offset += 1

            local_count_size = 1 + local_count
            if local_count != 0:
                for i in range(0, local_count):
                    partial_local_count = Conver2Int(
                        True, 1, code_section[6][offset:offset + 1])
                    temp_func_bodies.locals.append(deepcopy(partial_local_count))
                    offset += 1
                    offset += 1
                    local_count -= partial_local_count
                    local_count_size += 1
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

    def ReadDataSection(self):
        loop = True
        section_exists = False
        offset = 1
        DS = Data_Section()
        temp_data_segment = Data_Segment()
        init_expr = []
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 11:
                data_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        data_entry_count = data_section[6][offset]
        DS.count.append(data_entry_count)
        offset += 1

        while data_entry_count != 0:
            linear_memory_index = data_section[6][offset]
            temp_data_segment.index = linear_memory_index
            offset += 1

            while loop:
                if data_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(data_section[6][offset])
                offset += 1

            temp_data_segment.offset = init_expr

            data_entry_length = data_section[6][offset]
            temp_data_segment.size = data_entry_length
            offset += 1

            data_itself = data_section[6][offset:offset + data_entry_length]
            temp_data_segment.data = data_itself
            offset += data_entry_length

            DS.data_segments.append(deepcopy(temp_data_segment))

            data_entry_count -= 1
            init_expr = []
            loop = True
        return(DS)

    def ReadImportSection(self):
        offset = 1
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

        import_cnt = import_section[6][offset]
        IS.count.append(import_cnt)
        offset += 1

        while import_cnt != 0:
            module_length = import_section[6][offset]
            temp_import_entry.module_len = module_length
            offset += 1

            for i in range(0, module_length):
                module_name.append(import_section[6][offset + i])
            temp_import_entry.module_str = module_name
            offset += module_length

            field_length = import_section[6][offset]
            temp_import_entry.field_len = field_length
            offset += 1
            for i in range(0, field_length):
                field_name.append(import_section[6][offset + i])
            temp_import_entry.field_str = field_name
            offset += field_length

            kind = import_section[6][offset]
            temp_import_entry.kind = kind
            offset += 1

            yolo_byte = import_section[6][offset:offset + 1]
            temp_import_entry.type = yolo_byte
            offset += 1

            IS.import_entry.append(deepcopy(temp_import_entry))

            import_cnt -= 1
            module_name = []
            field_name = []
        return(IS)

    def ReadSectionExport(self):
        offset = 1
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

        export_entry_cnt = export_section[6][offset]
        ES.count.append(export_entry_cnt)
        offset += 1

        while export_entry_cnt != 0:
            field_length = export_section[6][offset]
            temp_export_entry.field_len = field_length
            offset += 1

            for i in range(0, field_length):
                field_name.append(export_section[6][offset + i])
            temp_export_entry.fiels_str = field_name
            offset += field_length

            kind = export_section[6][offset]
            temp_export_entry.kind = kind
            offset += 1

            index = export_section[6][offset]
            temp_export_entry.index = index
            offset += 1

            ES.export_entries.append(deepcopy(temp_export_entry))

            export_entry_cnt -= 1
            field_name = []
        return(ES)

    def ReadSectionType(self):
        offset = 1
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

        type_entry_count = type_section[6][offset]
        TS.count.append(type_entry_count)
        offset += 1

        while type_entry_count != 0:
            form = type_section[6][offset]
            temp_func_type.form = form
            offset += 1
            param_count = type_section[6][offset]
            temp_func_type.param_cnt = param_count
            offset += 1

            for i in range(0, param_count):
                param_list.append(type_section[6][offset + i])
            temp_func_type.param_types = param_list
            offset += param_count

            return_count = type_section[6][offset]
            temp_func_type.return_cnt = return_count
            offset += 1

            for i in range(0, return_count):
                return_list.append(type_section[6][offset + i])
            temp_func_type.return_type = return_list
            offset += return_count

            TS.func_types.append(deepcopy(temp_func_type))

            type_entry_count -= 1
            param_list = []
            return_list = []
        return(TS)

    def ReadSectionFunction(self):
        offset = 1
        section_exists = False
        index_to_type = []
        FS = Function_Section()
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 3:
                function_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        function_entry_count = function_section[6][offset]
        FS.count.append(function_entry_count)
        offset += 1

        for i in range(0, function_entry_count):
            index_to_type.append(function_section[6][offset + i])
        FS.type_section_index = index_to_type
        offset += function_entry_count
        return(FS)

    def ReadSectionElement(self):
        offset = 1
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

        element_entry_count = element_section[6][offset]
        ES.count.append(element_entry_count)
        offset += 1

        while element_entry_count != 0:
            table_index = element_section[6][offset]
            temp_elem_segment.index = table_index
            offset += 1

            while loop:
                if element_section[6][offset] == 0x0b:
                    loop = False
                init_expr.append(element_section[6][offset])
                offset += 1
            temp_elem_segment.offset = init_expr

            num_elements = element_section[6][offset]
            temp_elem_segment.num_elem = num_elements

            for i in range(0, num_elements):
                function_indices.append(element_section[6][offset + i])
            temp_elem_segment.elems = function_indices
            offset += num_elements

            ES.elem_segments.append(deepcopy(temp_elem_segment))

            loop = True
            init_expr = []
            function_indices = []
            element_entry_count -= 1
        return(ES)

    def ReadMemorySection(self):
        offset = 1
        section_exists = False
        MS = Memory_Section()
        temp_rsz_limits = Resizable_Limits()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 5:
                memory_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        num_linear_mems = memory_section[6][offset]
        MS.count.append(num_linear_mems)
        offset += 1

        while num_linear_mems != 0:
            flag = memory_section[6][offset]
            temp_rsz_limits.flags = flag
            offset += 1

            initial = LEB128UnsignedDecode(memory_section[6][offset:offset + 2])
            temp_rsz_limits.initial = initial
            offset += 2

            if flag == 1:
                maximum = LEB128UnsignedDecode(
                    memory_section[6][offset:offset + 2])
                temp_rsz_limits.maximum = maximum
                offset += 2

            MS.memory_types.append(deepcopy(temp_rsz_limits))
            num_linear_mems -= 1
        return(MS)

    def ReadSectionTable(self):
        offset = 1
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

        table_count = table_section[6][offset]
        TS.count.append(table_count)
        offset += 1

        while table_count != 0:
            element_type = table_section[6][offset]
            temp_table_type.element_type = element_type
            offset += 1

            flag = table_section[6][offset]
            temp_rsz_limits.flags = flag
            offset += 1

            initial = LEB128UnsignedDecode(table_section[6][offset:offset + 2])
            temp_rsz_limits.initial = initial
            offset += 2

            if flag == 1:
                maximum = LEB128UnsignedDecode(
                    table_section[6][offset:offset + 2])
                temp_rsz_limits.maximum = maximum
                offset += 2

            temp_table_type.limit = temp_rsz_limits
            TS.table_types.append(deepcopy(temp_table_type))

            table_count -= 1
        return(TS)

    def ReadSectionGlobal(self):
        offset = 1
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

        count = global_section[6][offset]
        GS.count.append(count)
        offset += 1

        while count != 0:
            content_type = global_section[6][offset]
            temp_gl_type.content_type = content_type
            offset += 1

            mutability = global_section[6][offset]
            temp_gl_type.mutability = mutability
            offset += 1

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

    def ReadStartSection(self):
        offset = 1
        section_exists = False
        SS = Start_Section()

        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 8:
                start_section = whatever.copy()
                section_exists = True

        if not section_exists:
            return None

        function_index = start_section[6][offset]
        SS.function_section_index.append(function_index)
        offset += 1
        return(SS)

    def getCursorLocation(self):
        return(self.wasm_file.tell())

    def parse(self):
        #self.parsedstruct.section_list = []
        return(Module(self.ReadSectionType(), self.ReadImportSection(),
                      self.ReadSectionFunction(), self.ReadSectionTable(),
                      self.ReadMemorySection(), self.ReadSectionGlobal(),
                      self.ReadSectionExport(), self.ReadStartSection(),
                      self.ReadSectionElement(), self.ReadCodeSection(),
                      self.ReadDataSection()))


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
    def __init__(self):
        self.modules = []

    def appendmodule(self, module):
        self.modules.append(module)

    def getmodules(self):
        return(self.modules)

    def parse(self, file_path):
        parser = ObjReader(ReadWASM(file_path, 'little', False, True))
        return(parser.parse())

    def dump_sections(self, module):
        print(Colors.blue + Colors.BOLD +
                'BEGENNING OF MODULE' + Colors.ENDC)

        # type_section
        if module.type_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Type Section:' + Colors.ENDC)
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
            print(Colors.blue + 'Import Section:' + Colors.ENDC)
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
            print(Colors.blue + 'Function Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.function_section.count))
            for iter in module.function_section.type_section_index:
                print(Colors.cyan + 'type section index: ' + repr(iter) + Colors.ENDC)

        # table_section
        if module.table_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Table Section:' + Colors.ENDC)
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
            print(Colors.blue + 'Memory Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.memory_section.count))
            for iter in module.memory_section.memory_types:
                print(Colors.green + 'Resizable_Limits:flags: ' + repr(iter.flags) + Colors.ENDC)
                print(Colors.red + 'Resizable_Limits:initial: ' + repr(iter.initial) + Colors.ENDC)
                print(Colors.purple + 'Resizable_Limits:maximum: ' + repr(iter.maximum) + Colors.ENDC)

        # global_section
        if module.global_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Global Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.global_section.count))
            for iter in module.global_section.global_variables:
                print(Colors.green + 'global type: ' + repr(iter.global_type) + Colors.ENDC)
                print(Colors.red + 'init expr: ' + repr(iter.init_expr) + Colors.ENDC)

        # export_section
        if module.export_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Export Section:' + Colors.ENDC)
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
            print(Colors.blue + 'Start Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('start function index: ' + repr(module.start_section.function_section_index))

        # element_section
        if module.element_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Element Section:' + Colors.ENDC)
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
            print(Colors.blue + 'Code Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.code_section.count))
            for iter in module.code_section.func_bodies:
                print(Colors.green + 'body_size: ' + repr(iter.body_size) + Colors.ENDC)
                print(Colors.red + 'local_count: ' + repr(iter.local_count) + Colors.ENDC)
                print(Colors.purple + 'locals: ' + repr(iter.locals) + Colors.ENDC)
                for iterer in iter.code:
                    print(Colors.cyan + 'opcode: ' + repr(iterer.opcode) + Colors.ENDC)
                    print(Colors.grey + 'code: ' + repr(iterer.operands) + Colors.ENDC)

        # data_section
        if module.data_section is not None:
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print(Colors.blue + 'Data Section:' + Colors.ENDC)
            print(Colors.blue + '------------------------------------------------------' + Colors.ENDC)
            print('count: ' + repr(module.data_section.count))
            for iter in module.data_section.data_segments:
                print(Colors.green + 'index: ' + repr(iter.index) + Colors.ENDC)
                print(Colors.red + 'offset: ' + repr(iter.offset) + Colors.ENDC)
                print(Colors.purple + 'size: ' + repr(iter.size) + Colors.ENDC)
                print(Colors.cyan + 'data:' + repr(iter.data) + Colors.ENDC)

    def runValidations(self):
        pass


def main():
    argparser = CLIArgParser()

    if argparser.getWASMPath() is not None:
        interpreter = PythonInterpreter()
        for file_path in argparser.getWASMPath():
            module = interpreter.parse(file_path)
            interpreter.appendmodule(module)
            interpreter.runValidations()
            if argparser.getDBG():
                interpreter.dump_sections(module)

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
