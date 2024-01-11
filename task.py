from enum import Enum
from promise import *

class TaskStatus(Enum):
    CREATED = 0
    READY = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4


class TaskType(Enum):
    STATIC = 0
    DYNAMIC = 1


class Task:
    def __init__(self, id: str, path: str):
        self.id = id
        self.path = path
        self.status = TaskStatus.CREATED

        self.type = TaskType.STATIC
        self.promise_task = STATIC
        self.cur_task = 0
        self.promise_edge = STATIC
        self.cur_edge = 0


    def add_promise(self, promise: Promise):
        if promise == Promise.STATIC:
            self.type = TaskType.STATIC
            self.promise_task = STATIC
            self.promise_edge = STATIC

        elif promise == Promise.DYNAMIC:
            self.type = TaskType.DYNAMIC
            self.promise_task = DYNAMIC
            self.promise_edge = DYNAMIC

        elif promise == Promise.NO_NEW_TASK:
            self.promise_task = STATIC
        
        elif promise == Promise.NO_NEW_EDGE:
            self.promise_task = STATIC
        
        elif promise == Promise.LIMITED_NEW_TASK:
            self.type = TaskType.DYNAMIC
            self.promise_task = LIMITED_DYNAMIC
        
        elif promise == Promise.LIMITED_NEW_EDGE:
            self.type = TaskType.DYNAMIC
            self.promise_edge = LIMITED_DYNAMIC
        

        if self.type == TaskType.DYNAMIC and self.promise_task == STATIC and self.promise_edge == STATIC:
            self.type = TaskType.STATIC


    def increase_task(self):
        self.cur_task += 1

    
    def increase_edge(self):
        self.cur_edge += 1

    
    def check_promises(self) -> bool:
        if self.cur_edge > self.promise_edge or self.cur_task > self.promise_task:
            return False
        return True



class TaskOutput:
    def __init__(self, task_id: str):
        self.id = task_id
        # json -> string
        self.data = None

