from enum import Enum

STATIC = 0
DYNAMIC = 10
LIMITED_DYNAMIC = 5

class Promise(Enum):
    STATIC = 0
    DYNAMIC = 1
    NO_NEW_TASK = 2
    NO_NEW_EDGE = 3
    LIMITED_NEW_TASK = 4
    LIMITED_NEW_EDGE = 5