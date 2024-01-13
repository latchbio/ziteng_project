from enum import IntEnum

STATIC = 0
LIMITED_DYNAMIC = 1
FULLY_DYNAMIC = 10

class Promise(IntEnum):
    STATIC = 0
    NO_NEW_TASK = 1
    NO_NEW_EDGE = 2
    LIMITED_NEW_TASK = 4
    LIMITED_NEW_EDGE = 5
    FULL_NEW_TASK = 6
    FULL_NEW_EDGE = 7
    KEEP_ONE_EDGE = 8