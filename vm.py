from OpCodes import WASM_OP_Code
from utils import Colors
from argparser import Read


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

