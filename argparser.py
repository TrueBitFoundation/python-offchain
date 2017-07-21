from __future__ import print_function
import argparse
import sys
import re

__DBG__ = True


class Colors:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    grey = '\033[1;37m'
    darkgrey = '\033[1;30m'
    cyan = '\033[1;36m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class WASM_OP_Code:
    magic_number = 0x6d736100
    version_number = 0x01
    uint8 = 1
    uint16 = 2
    uint32 = 4
    uint64 = 8
    varuint1 = 1
    varuint7 = 1
    varuint32 = 4
    varuint64 = 8
    varint1 = 1
    varint7 = 1
    varint32 = 4
    varint64 = 8

    all_ops = [('i32', '7f', False), ('i64', '7e', False), ('f32', '7d', False),
                ('f63', '7c', False), ('anyfunc', '7b', False),
                ('func', '60', False), ('empty_block_type', '40', False),
                ('unreachable', '00', False), ('nop', '01', False),
                ('block', '02', True, (varuint7)),
                ('loop', '03', True, (varuint7)),
                ('if', '04', True, (varuint7)), ('else', '05', False),
                ('end', '0b', False), ('br', '0c', True, (varuint32)),
                ('br_if', '0d', True, varuint32),
                ('br_table', '0e', True, (varuint32, varuint32, varuint32)),
                ('return', '0f', False), ('call', '10', True, (varuint32)),
                ('call_indirect', '11', True, (varuint32, varuint1)),
                ('drop', '1a', False), ('select', '1b', False),
                ('get_local', '20', True, (varuint32)),
                ('set_local', '21', True, (varuint32)),
                ('tee_local', '22', True, (varuint32)),
                ('get_global', '23', True, (varuint32)),
                ('set_global', '24', True, (varuint32)),
                ('i32.load', '28', True, (varuint32, varuint32)),
                ('i64.load', '29', True, (varuint32, varuint32)),
                ('f32.load', '2a', True, (varuint32, varuint32)),
                ('f64.load', '2b', True, (varuint32, varuint32)),
                ('i32.load8_s', '2c', True, (varuint32, varuint32)),
                ('i32.load8_u', '2d', True, (varuint32, varuint32)),
                ('i32.load16_s', '2e', True, (varuint32, varuint32)),
                ('i32.load16_u', '2f', True, (varuint32, varuint32)),
                ('i64.load8_s', '30', True, (varuint32, varuint32)),
                ('i64.load8_u', '31', True, (varuint32, varuint32)),
                ('i64.load16_s', '32', True, (varuint32, varuint32)),
                ('i64.load16_u', '33', True, (varuint32, varuint32)),
                ('i64.load32_s', '34', True, (varuint32, varuint32)),
                ('i64.load32_u', '35', True, (varuint32, varuint32)),
                ('i32.store', '36', True, (varuint32, varuint32)),
                ('i64.store', '37', True, (varuint32, varuint32)),
                ('f32.store', '38', True, (varuint32, varuint32)),
                ('f64.store', '39', True, (varuint32, varuint32)),
                ('i32.store8', '3a', True, (varuint32, varuint32)),
                ('i32.store16', '3b', True, (varuint32, varuint32)),
                ('i64.store8', '3c', True, (varuint32, varuint32)),
                ('i64.store16', '3d', True, (varuint32, varuint32)),
                ('i64.store32', '3e', True, (varuint32, varuint32)),
                ('current_memory', '3f', True, (varuint1)),
                ('grow_memory', '40', True, (varuint1)),
                ('i32.const', '41', True, (varint32)),
                ('i64.const', '42', True, (varint64)),
                ('f32.const', '43', True, (uint32)),
                ('f64', '44', True, (uint64)),
                ('i32.eqz', '45', False), ('i32.eq', '46', False),
                ('i32.ne', '47', False), ('i32.lt_s', '48', False),
                ('i31.lt_u', '49', False), ('i32.gt_s', '4a', False),
                ('i32.gt_u', '4b', False), ('i32.le_s', '4c', False),
                ('i32.le_u', '4d', False), ('i32.ge_s', '4e', False),
                ('i32.ge_u', '4f', False), ('i64.eqz', '50', False),
                ('i64.eq', '51', False), ('i64.ne', '52', False),
                ('i64.lt_s', '53', False), ('i64.lt_u', '54', False),
                ('i64.gt_s', '55', False), ('i64.gt_u', '56', False),
                ('i64.le_s', '57', False), ('i64.le_u', '58', False),
                ('i64.ge_s', '59', False), ('i64.ge_u', '5a', False),
                ('f32.eq', '5b', False), ('f32.ne', '5c', False),
                ('f32.lt', '5d', False), ('f32.gt', '5e', False),
                ('f32.le', '5f', False), ('f32.ge', '60', False),
                ('f64.eq', '61', False), ('f64.ne', '62', False),
                ('f64.lt', '63', False), ('f64.gt', '64', False),
                ('f64.le', '65', False), ('f64.ge', '66', False),
                ('i32.clz', '67', False), ('i31.ctz', '68', False),
                ('i32.popcnt', '69', False), ('i32.add', '6a', False),
                ('i32.sub', '6b', False), ('i32.mul', '6c', False),
                ('i32.div_s', '6d', False), ('i32.div_u', '6e', False),
                ('i32.rem_s', '6e', False), ('i32.rem_u', '70', False),
                ('i32.and', '71', False), ('i32.or', '72', False),
                ('i32.xor', '73', False), ('i32.shl', '74', False),
                ('i32.shr_s', '75', False), ('i32.shr_u', '76', False),
                ('i32.rotl', '77', False), ('i32.rotr', '78', False),
                ('i64.clz', '79', False), ('i64.ctz', '7a', False),
                ('i64.popcnt', '7b', False), ('i64.add', '7c', False),
                ('i64.sub', '7d', False), ('i64.mul', '7e', False),
                ('i64.div_s', '7f', False), ('i64.div_u', '80', False),
                ('i64.rem_s', '81', False), ('i64.rem_u', '82', False),
                ('i64.and', '83', False), ('i64.or', '84', False),
                ('i64.xor', '85', False), ('i64.shl', '86', False),
                ('i64.shr_s', '87', False), ('i64.shr_u', '88', False),
                ('i64.rotl', '89', False), ('i63.rotr', '8a', False),
                ('f32.abs', '8b', False), ('f32.neg', '8c', False),
                ('f32.ceil', '8d', False),  ('f32.floor', '8e', False),
                ('f32.trunc', '8f', False), ('f32.nearest', '90', False),
                ('f32.sqrt', '91', False), ('f32.add', '92', False),
                ('f32.sub', '93', False), ('f32.mul', '94', False),
                ('f32.div', '95', False), ('f32.min', '96', False),
                ('f32.max', '97', False), ('f32.copysign', '98', False),
                ('f64.abs', '99', False), ('f64.neg', '9a', False),
                ('f64.ceil', '9b', False), ('f64.floor', '9c', False),
                ('f64.trunc', '9d', False), ('f64.nearest', '9e', False),
                ('f64.sqrt', '9f', False), ('f64.add', 'a0', False),
                ('f64.sub', 'a1', False), ('f64.mul', 'a2', False),
                ('f64.div', 'a3', False), ('f64.min', 'a4', False),
                ('f64.max', 'a5', False), ('f64.copysign', 'a6', False),
                ('i32.wrap/i64', 'a7', False), ('i32.trunc_s/f32', 'a8', False),
                ('i32.trunc_u/f32', 'a9', False),
                ('i32.trunc_s/f64', 'aa', False),
                ('i32.trunc_u/f64', 'ab', False),
                ('i64.extend_s/i32', 'ac', False),
                ('i64.extend_u/i32', 'ad', False),
                ('i64.trunc_s/f32', 'ae', False),
                ('i64.trunc_u/f32', 'af', False),
                ('i64.trunc_s/f64', 'b0', False),
                ('i64.trunc_u/f64', 'b1', False),
                ('f32.convert_s/i32', 'b2', False),
                ('f32.convert_u/i32', 'b3', False),
                ('f32.convert_s/i64', 'b4', False),
                ('f32.convert_u/i64', 'b5', False),
                ('f32.demote/f64', 'b6', False),
                ('f64.convert_s/i32', 'b7', False),
                ('f64.convert_u/i32', 'b8', False),
                ('f64.convert_s/i64', 'b9', False),
                ('f64.convert_u/i64', 'ba', False),
                ('f64.promote/f32', 'bb', False),
                ('i32.reinterpret/f32', 'bc', False),
                ('i64.reinterpret/f64', 'bd', False),
                ('f32.reinterpret/i32', 'be', False),
                ('f64.reinterpret/i64', 'bf', False)]

    type_ops = [('i32', '7f'), ('i64', '7e'), ('f32', '7d'),
                ('f64', '7c'), ('anyfunc', '7b'), ('func', '60'),
                ('empty_block_type', '40')]
    type_ops_dict = dict(type_ops)
    type_ops_dict_rev = {v: k for k, v in type_ops_dict.items()}

    control_flow_ops = [('unreachable', '00'), ('nop', '01'),
                        ('block', '02'), ('loop', '03'),
                        ('if', '04'), ('else', '05'),
                        ('end', '0b'), ('br', '0c'),
                        ('br_if', '0d'), ('br_table', '0e'),
                        ('return', '0f')]
    control_flow_ops_dict = dict(control_flow_ops)
    control_flow_ops_dict_rev = {v: k for k, v in control_flow_ops_dict.items()}

    call_ops = [('call', '10'), ('call_indirect', '11')]
    call_ops_dict = dict(call_ops)
    call_ops_dict_rev = {v: k for k, v in call_ops_dict.items()}

    param_ops = [('drop', '1a'), ('select', '1b')]
    param_ops_dict = dict(param_ops)
    param_ops_dict_rev = {v: k for k, v in param_ops_dict.items()}

    var_access = [('get_local', '20'), ('set_local', '21'),
                    ('tee_local', '22'), ('get_global', '23'),
                    ('set_global', '24')]
    var_access_dict = dict(var_access)
    var_access_dict_rev = {v: k for k, v in var_access_dict.items()}

    mem_ops = [('i32.load', '28'), ('i64.load', '29'),
                ('f32.load', '2a'), ('f64.load', '2b'),
                ('i32.load8_s', '2c'), ('i32.load8_u', '2d'),
                ('i32.load16_s', '2e'),  ('i32.load16_u', '2f'),
                ('i64.load8_s', '30'), ('i64.load8_u', '31'),
                ('i64.load16_s', '32'), ('i64.load16_u', '33'),
                ('i64.load32_s', '34'), ('i64.load32_u', '35'),
                ('i32.store', '36'), ('i64.store', '37'),
                ('f32.store', '38'), ('f64.store', '39'),
                ('i32.store8', '3a'), ('i32.store16', '3b'),
                ('i64.store8', '3c'), ('i64.store16', '3d'),
                ('i64.store32', '3e'), ('current_memory', '3f'),
                ('grow_memory', '40')]
    mem_ops_dict = dict(mem_ops)
    mem_ops_dict_rev = {v: k for k, v in mem_ops_dict.items()}

    consts = [('i32.const', '41'), ('i64.const', '42'),
              ('f32.const', '43'), ('f64', '44')]
    consts_dict = dict(consts)
    consts_dict_rev = {v: k for k, v in consts_dict.items()}

    comp_ops = [('i32.eqz', '45'), ('i32.eq', '46'), ('i32.ne', '47'),
                ('i32.lt_s', '48'), ('i32.lt_u', '49'),
                ('i32.gt_s', '4a'), ('i32.gt_u', '4b'),
                ('i32.le_s', '4c'), ('i32.le_u', '4d'),
                ('i32.ge_s', '4e'), ('i32.ge_u', '4f'),
                ('i64.eqz', '50'), ('i64.eq', '51'),
                ('i64.ne', '52'), ('i64.lt_s', '53'),
                ('i64.lt_u', '54'), ('i64.gt_s', '55'),
                ('i64.gt_u', '56'), ('i64.le_s', '57'),
                ('i64.le_u', '58'), ('i64.ge_s', '59'),
                ('i64.ge_u', '5a'), ('f32.eq', '5b'),
                ('f32.ne', '5c'), ('f32.lt', '5d'),
                ('f32.gt', '5e'), ('f32.le', '5f'),
                ('f32.ge', '60'), ('f64.eq', '61'),
                ('f64.ne', '62'), ('f64.lt', '63'),
                ('f64.gt', '64'), ('f64.le', '65'),
                ('f64.ge', '66')]
    comp_ops_dict = dict(comp_ops)
    comp_ops_dict_rev = {v: k for k, v in comp_ops_dict.items()}

    num_ops = [('i32.clz', '67'), ('i32.ctz', '68'),
               ('i32.popcnt', '69'), ('i32.add', '6a'),
               ('i32.sub', '6b'), ('i32.mul', '6c'),
               ('i32.div_s', '6d'), ('i32.div_u', '6e'),
               ('i32.rem_s', '6e'), ('i32.rem_u', '70'),
               ('i32.and', '71'), ('i32.or', '72'),
               ('i32.xor', '73'), ('i32.shl', '74'),
               ('i32.shr_s', '75'), ('i32.shr_u', '76'),
               ('i32.rotl', '77'), ('i32.rotr', '78'),
               ('i64.clz', '79'), ('i64.ctz', '7a'),
               ('i64.popcnt', '7b'), ('i64.add', '7c'),
               ('i64.sub', '7d'), ('i64.mul', '7e'),
               ('i64.div_s', '7f'), ('i64.div_u', '80'),
               ('i64.rem_s', '81'), ('i64.rem_u', '82'),
               ('i64.and', '83'), ('i64.or', '84'),
               ('i64.xor', '85'), ('i64.shl', '86'),
               ('i64.shr_s', '87'), ('i64.shr_u', '88'),
               ('i64.rotl', '89'), ('i63.rotr', '8a'),
               ('f32.abs', '8b'), ('f32.neg', '8c'),
               ('f32.ceil', '8d'),  ('f32.floor', '8e'),
               ('f32.trunc', '8f'), ('f32.nearest', '90'),
               ('f32.sqrt', '91'), ('f32.add', '92'),
               ('f32.sub', '93'), ('f32.mul', '94'),
               ('f32.div', '95'), ('f32.min', '96'),
               ('f32.max', '97'), ('f32.copysign', '98'),
               ('f64.abs', '99'), ('f64.neg', '9a'),
               ('f64.ceil', '9b'), ('f64.floor', '9c'),
               ('f64.trunc', '9d'), ('f64.nearest', '9e'),
               ('f64.sqrt', '9f'), ('f64.add', 'a0'),
               ('f64.sub', 'a1'), ('f64.mul', 'a2'),
               ('f64.div', 'a3'), ('f64.min', 'a4'),
               ('f64.max', 'a5'), ('f64.copysign', 'a6')]
    num_ops_dict = dict(num_ops)
    num_ops_dict_rev = {v: k for k, v in num_ops_dict.items()}

    conversion = [('i32.wrap/i64', 'a7'),
                    ('i32.trunc_s/f32', 'a8'),
                    ('i32.trunc_u/f32', 'a9'),
                    ('i32.trunc_s/f64', 'aa'),
                    ('i32.trunc_u/f64', 'ab'),
                    ('i64.extend_s/i32', 'ac'),
                    ('i64.extend_u/i32', 'ad'),
                    ('i64.trunc_s/f32', 'ae'),
                    ('i64.trunc_u/f32', 'af'),
                    ('i64.trunc_s/f64', 'b0'),
                    ('i64.trunc_u/f64', 'b1'),
                    ('f32.convert_s/i32', 'b2'),
                    ('f32.convert_u/i32', 'b3'),
                    ('f32.convert_s/i64', 'b4'),
                    ('f32.convert_u/i64', 'b5'),
                    ('f32.demote/f64', 'b6'),
                    ('f64.convert_s/i32', 'b7'),
                    ('f64.convert_u/i32', 'b8'),
                    ('f64.convert_s/i64', 'b9'),
                    ('f64.convert_u/i64', 'ba'),
                    ('f64.promote/f32', 'bb')]
    conversion_dict = dict(conversion)
    conversion_dict_rev = {v: k for k, v in conversion_dict.items()}

    reinterpretations = [('i32.reinterpret/f32', 'bc'),
                         ('i64.reinterpret/f64', 'bd'),
                         ('f32.reinterpret/i32', 'be'),
                         ('f64.reinterpret/i64', 'bf')]
    reinterpretations_dict = dict(reinterpretations)
    reinterpretations_dict_rev = {v: k for k,
                                  v in reinterpretations_dict.items()}

    section_code = [('type', '01'), ('import', '02'),
                    ('function', '03'), ('table', '04'),
                    ('memory', '05'), ('global', '06'),
                    ('export', '07'), ('start', '08'),
                    ('element', '09'), ('code', '0a'),
                    ('data', '0b'), ('custom', '00')]
    section_code_dict = dict(section_code)
    section_code_dict_rev = {v: k for k, v in section_code_dict.items()}


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


def LEB128UnsingedDecode(bytelist):
    result = 0
    shift = 0
    for byte in bytelist:
        result |= (byte & 0x7f) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return(result)


def LEB128SingedDecode(bytelist):
    result = 0
    shift = 0
    for byte in bytelist:
        result |= (byte & 0x7f) << shift
        last_byte = byte
        shift += 7
        if (byte & 0x80) == 0:
            break

    if (shift < len(bytelist.len()*8)) and (last_byte & 0x40 == 0x40):
        result |= - (1 << shift)

    return(result)


def LEB128UnsingedEncode(int_val, num_byte):
    byte_array = bytearray()
    return(byte_array)
    pass


def LEB128SingedEncode(int_val, num_byte):
    byte_array = bytearray()
    return(byte_array)
    pass


class CLIArgParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--wast", type=str,
                            help="path to the wasm text file")
        parser.add_argument("--wasm", type=str,
                            help="path to the wasm object file")
        parser.add_argument("--asb", type=str,
                            help="path to the wast file to assemble")
        parser.add_argument("--dis", type=str,
                            help="path to the wasm file to disassemble")
        parser.add_argument("-o", type=str, help="the path to the output file")

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

    def __init__(self, file_path, endianness, is_extended_isa):
        self.wasm_file = open(file_path, "rb")
        self.file_path = file_path
        self.endianness = endianness
        self.is_extended_isa = is_extended_isa

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
            section_id_int = LEB128UnsingedDecode(section_id)

            payload_length = self.wasm_file.read(WASM_OP_Code.varuint32)
            payload_length_int = LEB128UnsingedDecode(payload_length) + 1
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
                        for i in op_code[3]:
                            byte = LEB128UnsingedDecode(
                                section_byte[offset:offset + i])
                            instruction += repr(byte) + ' '
                            offset += i
                            read_bytes += i
                            print(i)
                    else:
                        byte = LEB128UnsingedDecode(
                            section_byte[6][offset:offset + op_code[3]])
                        instruction += repr(byte) + ' '
                        print (LEB128UnsingedDecode(
                            section_byte[6][offset: offset + op_code[3]]))
                        offset += op_code[3]
                        read_bytes += op_code[3]

                print(Colors.green +
                      op_code[0] + ' ' + instruction + Colors.ENDC)
                instruction = str()
                break

        print('read bytes this iteration:' + repr(read_bytes))
        return offset, matched, read_bytes

    def ReadCodeSection(self):
        offset = 1
        for whatever in self.parsedstruct.section_list:
            # 10 is the code section
            if whatever[0] == 10:
                code_section = whatever.copy()
        print(code_section)

        function_cnt = LEB128UnsingedDecode(code_section[6][offset:offset + 1])
        offset += 1
        print('function count :' + repr(function_cnt))

        while function_cnt > 0:
            print(code_section[6][offset:offset + 4])
            function_body_length = LEB128UnsingedDecode(
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

            read_bytes_so_far = int()
            print(Colors.purple + repr(local_count_size) + Colors.ENDC)
            for i in range(0, function_body_length - local_count_size):
                if read_bytes_so_far >= function_body_length - local_count_size:
                    break
                print('----------------------------------------')

                offset, matched, read_bytes = self.Disassemble(
                    code_section, offset)

                if not matched:
                    print(Colors.red + 'did not match anything' + Colors.ENDC)
                else:
                    print(Colors.yellow + 'matched something' + Colors.ENDC)
                matched = False
                read_bytes_so_far += read_bytes

            function_cnt -= 1

    def ReadDataSection(self):
        for whatever in self.parsedstruct.section_list:
            if whatever[0] == 11:
                data_section = whatever.copy()

        data_cnt = LEB128UnsingedDecode(data_section[6][1:2])
        print(data_cnt)

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
        wasmobj = ObjReader(argparser.getWASMPath(), 'little', False)
        # wasmobj.testprintall()
        # wasmobj.testprintbyteall()
        wasmobj.ReadWASM()
        # wasmobj.PrintAllSection()
        wasmobj.ReadCodeSection()
        wasmobj.ReadDataSection()


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
