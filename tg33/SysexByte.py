from enum import Enum

class SysexByte(Enum):
    START = 0xF0
    YAMAHA = 0x43
    DEVICE = 0x00
    BULK = 0x7E
    END = 0xF7
