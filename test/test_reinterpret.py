import sys
sys.path.append('../')
from utils import Colors, reinterpretf32toi32, reinterpretf64toi64, reinterpreti32tof32, reinterpreti64tof64


def test_reintf32toi32():
    val = 12345.6789
    print(reinterpretf32toi32(val))


def test_reintf64toi64():
    val = 12345.6789
    print(reinterpretf64toi64(val))


def test_reinti32tof32():
    val = 123456789
    print(reinterpreti32tof32(val))


def test_reinti64tof64():
    val = 123456789
    print(reinterpreti64tof64(val))


def main():
    test_reintf32toi32()
    test_reintf64toi64()
    test_reinti32tof32()
    test_reinti64tof64()

if __name__ == '__main__':
    main()
