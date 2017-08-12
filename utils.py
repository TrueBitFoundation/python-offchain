from OpCodes import *


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


# @DEVI-FIXME-MVP-only
def init_interpret(expr):
    offset = 0
    byte, offset, dummy = Read(expr, offset, 'uint8')
    const = int()

    if byte == 65:
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

