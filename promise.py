from enum import IntEnum

STATIC = 0
LIMITED_DYNAMIC = 5
FULLY_DYNAMIC = 10

class Promise(IntEnum):
    STATIC = 0
    BRANCH = 1
    MAP_TASK = 2
    NO_NEW_TASK = 3
    NO_NEW_EDGE = 4
    LIMITED_NEW_TASK = 5
    LIMITED_NEW_EDGE = 6