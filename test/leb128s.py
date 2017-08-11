import sys
sys.path.append('../')
from utils import *

def leb128sencodedecodeexhaustive():
    failed = False
    for i in range(-25600, 25600):
        a = LEB128SignedEncode(i)
        b = LEB128SignedDecode(LEB128SignedEncode(i))
        if i != b:
            print('encoded/decoded pair not matching')
            print(i)
            print(repr(i) + '  ' + repr(LEB128SignedEncode(i)))
            print(LEB128SignedDecode(LEB128SignedEncode(i)))
            print('--------------------------------------')
            failed = True

    return(failed)

def leb128uencodedecodeexhaustive():
    failed = False
    for i in range(0, 25600):
        b = LEB128UnsignedDecode(LEB128UnsignedEncode(i))
        if i != b:
            print('encoded/decoded pair not matching')
            print(i)
            print(repr(i) + '  ' + repr(LEB128UnsignedEncode(i)))
            print(LEB128UnsignedDecode(LEB128UnsignedEncode(i)))
            print('--------------------------------------')
            failed = True


def main():
    leb128sencodedecodeexhaustive()
    leb128uencodedecodeexhaustive()

if __name__ == '__main__':
    main()
