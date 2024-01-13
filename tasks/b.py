import api
import json
import sys

cur_task = json.loads(sys.argv[1])[0]
inputs = json.loads(sys.argv[2])
print(f"Task B is executing! Task Id: {cur_task}, Input: {inputs}", file=sys.stderr)

indicator = inputs[0]
next_tasks = json.loads(sys.argv[1])[1]

if indicator % 2 == 0:
    api.remove_task(next_tasks[0])
else:
    api.remove_task(next_tasks[0])
