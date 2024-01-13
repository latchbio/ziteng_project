import api.api as api
import json
import sys
import util.utils as utils

cur_task = json.loads(sys.argv[1])[0]
inputs = json.loads(sys.argv[2])
print(f"Task C is executing! Task Id: {cur_task}, Input: {inputs}", file=sys.stderr)

indicator = inputs[0]
next_tasks = json.loads(sys.argv[1])[1]

for i in range(0, indicator):
    task_d = utils.generate_task_id("d")
    api.add_task(task_d, "src/tasks/d.py", [i])
    api.add_edge(cur_task, task_d)
    for next in next_tasks:
        api.add_edge(task_d, next)

for next in next_tasks:
    api.remove_edge(cur_task, next)
