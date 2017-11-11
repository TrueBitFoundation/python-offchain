from OpCodes import *
import numpy as np
import struct as stc


class ParseFlags:
    def __init__(self, wast_path, wasm_path, as_path, disa_path, out_path, dbg, unval, memdump
                 , idxspc, run, metric, gas, entry):
        self.wast_path = wast_path
        self.wasm_path = wasm_path
        self.as_path = as_path
        self.disa_path = disa_path
        self.out_path = out_path
        self.dbg = dbg
        self.unval = unval
        self.memdump = memdump
        self.idxspc = idxspc
        self.run = run
        self.metric = metric
        self.gas = gas
        self.entry = entry


# pretty print
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


def LEB128UnsignedDecode(bytelist):
    result = 0
    shift = 0
    for byte in bytelist:
        result |= (byte & 0x7f) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return(result)


def LEB128SignedDecode(bytelist):
    result = 0
    shift = 0
    for byte in bytelist:
        result |= (byte & 0x7f) << shift
        last_byte = byte
        shift += 7
        if (byte & 0x80) == 0:
            break

    if last_byte & 0x40:
        result |= - (1 << shift)

    return(result)


def LEB128UnsignedEncode(int_val):
    if int_val < 0:
        raise Exception("value must not be negative")
    elif int_val == 0:
        return bytes([0])

    byte_array = bytearray()
    while int_val:
        byte = int_val & 0x7f
        byte_array.append(byte | 0x80)
        int_val >>= 7

    byte_array[-1] ^= 0x80

    return(byte_array)


def LEB128SignedEncode(int_val):
    byte_array = bytearray()
    while True:
        byte = int_val & 0x7f
        byte_array.append(byte | 0x80)
        int_val >>= 7
        if (int_val == 0 and byte&0x40 == 0) or (int_val == -1 and byte&0x40):
            byte_array[-1] ^= 0x80
            break

    return(byte_array)


# @DEVI-FIXME-MVP-only-we currently inly support consts and get_global
# interprets the init-exprs
def init_interpret(expr):
    offset = 0
    byte, offset, dummy = Read(expr, offset, 'uint8')
    const = int()

    if byte == 65:
        # @DEVI-FIXME-the spec says varint32, obviously we are not doing that
        # since it will return neg values which are meningless and break things
        const, offset, dummy = Read(expr, offset, 'varuint32')
    elif byte == 66:
        const, offset, dummy = Read(expr, offset, 'varint64')
    elif byte == 67:
        const, offset, dummy = Read(expr, offset, 'uint32')
    elif byte == 68:
        const, offset, dummy = Read(expr, offset, 'uint64')
    elif byte == 35:
        pass
    else:
        raise Exception(Colors.red + "illegal opcode for an MVP init expr." + Colors.ENDC)

    block_end, offset, dummy = Read(expr, offset, 'uint8')
    if block_end != 11:
        raise Exception(Colors.red + "init expr has no block end." + Colors.ENDC)

    return(const)


# reads different-typed values from a byte array, takes in the bytearray, the
# current offset the read should be performed from and the kind of value that
# should be read. returns the read value as a decimal number, the updated
# offset and the number of bytes read
def Read(section_byte, offset, kind):
    operand = []
    return_list = int()
    read_bytes = 0

    if kind == 'varuint1' or kind == 'varuint7' or kind == 'varuint32' or kind == 'varuint64':
        while True:
            byte = int(section_byte[offset])
            read_bytes += 1
            offset += 1

            operand.append(byte)

            if byte == 0x80:
                pass
            elif byte & 0x80 != 0:
                pass
            else:
                # we have read the last byte of the operand
                break

        return_list = LEB128UnsignedDecode(operand)
        operand = []
    elif kind == 'uint8' or kind == 'uint16' or kind == 'uint32' or kind == 'uint64':
        byte = section_byte[offset: offset + TypeDic[kind]]
        read_bytes += TypeDic[kind]
        offset += TypeDic[kind]
        operand.append(byte)
        return_list = int.from_bytes(operand[0], byteorder='little', signed=False)
        operand = []
    elif kind == 'varint1' or kind == 'varint7' or kind == 'varint32' or kind == 'varint64':
        while True:
            byte = int(section_byte[offset])
            read_bytes += 1
            offset += 1

            operand.append(byte)

            # @DEVI-what happens when we decode a 56-bit value?
            if byte == 0x80 or byte == 0xff:
                pass
            elif byte & 0x80 != 0:
                pass
            else:
                # we have read the lasy byte of the operand
                break

        return_list = LEB128SignedDecode(operand)
        operand = []

    return return_list, offset, read_bytes


def ror(val, type_length, rot_size):
    rot_size_rem = rot_size % type_length
    return (((val >> rot_size_rem) & (2**type_length - 1)) | ((val & (2**rot_size_rem - 1)) << (type_length - rot_size_rem)))


def rol(val, type_length, rot_size):
    rot_size_rem = rot_size % type_length
    return (((val << rot_size_rem) & (2**type_length - 1)) | ((val & ((2**type_length - 1) - (2**(type_length - rot_size_rem) - 1))) >> (type_length - rot_size_rem)))


# @DEVI-these are here because i wanted to test them to make sure what i thik is
# happening is really happening
def reinterpretf32toi32(val):
    return (stc.unpack("i", stc.pack("f" ,val))[0])


def reinterpretf64toi64(val):
    return (stc.unpack("Q", stc.pack("d", val))[0])


def reinterpreti32tof32(val):
    return (stc.unpack("f", stc.pack("i", val))[0])


def reinterpreti64tof64(val):
    return (stc.unpack("d", stc.pack("Q", val))[0])


def clz(val, _type):
    cnt = int()
    if _type == 'uint32':
        bits = np.uint32(val)
        power = 31
        while power > -1:
            if val & 2**power == 0:
                cnt += 1
            else:
                break
            power -= 1
    elif _type == 'uint64':
        bits = bin(np.uint64(val))
        power = 63
        while power > -1:
            if val & 2**power == 0:
                cnt += 1
            else:
                break
            power -= 1
    else:
        raise Exception(Colors.red + "unsupported type passed to clz." + Colors.ENDC)
    return cnt


def ctz(val, _type):
    cnt = int()
    power = int()
    if _type == 'uint32':
        bits = np.uint32(val)
        while power < 32:
            if val & 2**power == 0:
                cnt += 1
            else:
                break
            power += 1
    elif _type == 'uint64':
        bits = bin(np.uint64(val))
        while power < 64:
            if val & 2**power == 0:
                cnt += 1
            else:
                break
            power += 1
    else:
        raise Exception(Colors.red + "unsupported type passed to ctz." + Colors.ENDC)
    return cnt


def pop_cnt(val, _type):
    cnt = int()
    power = int()
    if _type == 'uint32':
        bits = np.uint32(val)
        while power < 32:
            if val & 2**power != 0:
                cnt += 1
            power += 1
    elif _type == 'uint64':
        bits = bin(np.uint64(val))
        while power < 64:
            if val & 2**power != 0:
                cnt += 1
        power += 1
    else:
        raise Exception(Colors.red + "unsupported type passed to pop_cnt." + Colors.ENDC)
    return cnt
