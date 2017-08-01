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
