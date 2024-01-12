from api import *
import sys
import utils

cur_task = sys.argv[1]
print(f"Task C is executing! Task Id: {cur_task}", file=sys.stderr)

task_d = utils.generate_task_id("d")

add_task(task_d, "tasks/d.py", cur_task)
add_edge(cur_task, task_d, cur_task)