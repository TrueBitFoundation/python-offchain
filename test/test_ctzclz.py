import sys
sys.path.append('../')
from utils import Colors, clz, ctz, pop_cnt


def testclz():
    val = 123456789
    print(clz(val, "uint32"))


def testctz():
    val = 123456789
    print(ctz(val, "uint32"))


def testpop_cnt():
    val = 123456789
    print(pop_cnt(val, "uint32"))
    print(bin(val))


def main():
    testclz()
    testctz()
    testpop_cnt()

if __name__ == '__main__':
    main()
