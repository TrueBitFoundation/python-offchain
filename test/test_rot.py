import sys
sys.path.append('../')
from utils import Colors, ror, rol


def test_ror():
    print('----------------------------')
    failed = False
    print(bin(123456789))
    res = ror(123456789, 64, 10)
    print(bin(res))
    print('----------------------------')


def test_rol():
    print('----------------------------')
    failed = False
    print(bin(123456789))
    res = rol(123456789, 32, 10)
    print(bin(res))
    pass
    print('----------------------------')


def main():
    test_ror()
    test_rol()

if __name__ == '__main__':
    main()
