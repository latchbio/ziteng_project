from enum import Enum

# def task(func):
#     @functools.wraps(func)
#     def task_wrapper_decorator(*args, **kwargs):
#         task = Task(func)
#         manager.register(task)
        
#         # for arg in list(args)

#         return task.output
    
#     return task_wrapper_decorator



# def dynamic(func):
#     @functools.wraps(func)
#     def task_wrapper_decorator(*args, **kwargs):
#         #...
#         task = Task(func)
    
#     return task_wrapper_decorator


class TaskStatus(Enum):
    CREATED = 0
    READY = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4



class Task:
    def __init__(self, id, path):
        self.id = id
        self.path = path
        self.status = TaskStatus.CREATED
        


class TaskOutput:
    def __init__(self, task_id: str):
        self.id = task_id
        # json -> string
        self.data = None

