import api
import json
import sys
import utils

cur_task = json.loads(sys.argv[1])[0]
inputs = json.loads(sys.argv[2])
print(f"Task B is executing! Task Id: {cur_task}, Input: {inputs}", file=sys.stderr)

task_d = utils.generate_task_id("d")
task_e = utils.generate_task_id("e")

indicator = inputs[0]

if indicator % 2 == 0:
    api.add_task(task_d, "tasks/d.py")
    api.add_edge(cur_task, task_d)
else:
    api.add_task(task_e, "tasks/e.py")
    api.add_edge(cur_task, task_e)