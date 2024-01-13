from enum import Enum
from promise import *

# for status and graph display
class TaskStatus(Enum):
    CREATED = "lightcyan"
    READY = "skyblue"
    RUNNING = "orange"
    SUCCESS = "palegreen"
    FAILED = "firebrick1"


class Task:
    def __init__(self, id: str, path: str, input):
        self.id = id
        self.path = path
        self.status = TaskStatus.CREATED
        self.next_edges = 0
        self.inputs = [input] if input is not None else []
        self.output = None

        self.promise_new_task = STATIC
        self.new_tasks = 0
        self.promise_new_edge = STATIC
        self.new_edges = 0
        self.promise_edge = FULLY_DYNAMIC


    def add_promise(self, promise: Promise):
        if promise == Promise.STATIC:
            self.promise_new_task = STATIC
            self.promise_new_edge = STATIC

        elif promise == Promise.NO_NEW_TASK:
            self.promise_new_task = STATIC
        
        elif promise == Promise.NO_NEW_EDGE:
            self.promise_new_task = STATIC
        
        elif promise == Promise.LIMITED_NEW_TASK:
            self.promise_new_task = LIMITED_DYNAMIC
        
        elif promise == Promise.LIMITED_NEW_EDGE:
            self.promise_new_edge = LIMITED_DYNAMIC

        elif promise == Promise.FULL_NEW_TASK:
            self.promise_new_task = FULLY_DYNAMIC
        
        elif promise == Promise.FULL_NEW_EDGE:
            self.promise_new_edge = FULLY_DYNAMIC
        
        elif promise == Promise.KEEP_ONE_EDGE_RUNTIME:
            self.promise_edge = 1


    def increase_task(self):
        self.new_tasks += 1
    
    def increase_edge(self):
        self.new_edges += 1

    def decrease_edge(self):
        self.new_edges -= 1
    
    def check_promises(self) -> bool:
        if self.new_tasks > self.promise_new_task:
            print(f"Promise Violated:\n promised tasks: {self.promise_new_task}, new edges: {self.new_tasks}")
            return False
        elif self.new_edges > self.promise_new_edge:
            print(f"Promise Violated:\n promised edges: {self.promise_new_edge}, new edges: {self.new_edges}")
            return False
        elif self.status == TaskStatus.SUCCESS and self.next_edges > self.promise_edge:
            print(f"Promise Violated:\n promised edges: {self.promise_edge}, current edges: {self.next_edges}")
            return False

        
        return True
