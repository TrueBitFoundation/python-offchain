import sys
sys.path.append('../')

from utils import *
from binascii import hexlify

vals = [-624485, -1, 0, 1, 624485]
uResults = [None,
            None,
            bytes([0x00]),
            bytes([0x01]),
            bytes([0xE5,0x8E,0x26])]
sResults = [bytes([0x9B,0xF1,0x59]),
            bytes([0x7F]),
            bytes([0x00]),
            bytes([0x01]),
            bytes([0xE5,0x8E,0x26])]

success = Colors.green + "SUCCESS: " + Colors.ENDC
fail = Colors.red + "FAIL: " + Colors.ENDC

def test_unsigned_LEB128():
    for idx,val in enumerate(vals):
        try:
            result = LEB128UnsignedEncode(val)
            if result != uResults[idx]:
                print(fail + "result from LEB128UnsignedEncode (%s) failed to "
                      "provide correct output (%s)" %
                      (hexlify(result),hexlify(uResults[idx])))
                continue
            else:
                print(success + "result from LEB128UnsignedEncode is correct")

            res = LEB128UnsignedDecode(result)
            if res != val:
                print(fail + "result from LEB128UnsignedDecode (%d) failed to "
                      "provide correct output (%d)" % (res, val))
            else:
                print(success + "result from LEB128UnsignedDecode is correct")

        except:
            if val < 0:
                print(success + "%d properly identified as negative and threw "
                      "exception" % val)
            else:
                print(fail + "%d could not be encoded properly")

def test_signed_LEB128():
    for idx,val in enumerate(vals):
        try:
            result = LEB128SignedEncode(val)
            if result != sResults[idx]:
                print(fail + "result from LEB128SignedEncode (%s) failed to "
                      "provide correct output (%s)" %
                      (hexlify(result),hexlify(sResults[idx])))
                continue
            else:
                print(success + "result from LEB128SignedEncode is correct")

            res = LEB128SignedDecode(result)
            if res != val:
                print(fail + "result from LEB128SignedDecode (%d) failed to "
                      "provide correct output (%d)" % (res, val))
            else:
                print(success + "result from LEB128SignedDecode is correct")

        except:
            if val < 0:
                print(success + "%d properly identified as negative and threw "
                      "exception" % val)
            else:
                print(fail + "%d could not be encoded properly")

def main():
    test_unsigned_LEB128()
    test_signed_LEB128()

if __name__ == '__main__':
    main()
