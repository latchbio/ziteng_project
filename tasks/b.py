from api import *
import sys
import utils

cur_task = sys.argv[1]
print(f"Task B is executing! Task Id: {cur_task}", file=sys.stderr)

task_c = utils.generate_task_id("c")

add_task(task_c, "tasks/c.py", cur_task)
add_edge(cur_task, task_c, cur_task)
add_promise(task_c, Promise.DYNAMIC)