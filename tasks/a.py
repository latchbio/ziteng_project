import api
import json
import random
import sys

cur_task = json.loads(sys.argv[1])[0]
inputs = json.loads(sys.argv[2])
print(f"Task A is executing! Task Id: {cur_task}, Input: {inputs}", file=sys.stderr)

num = inputs[0]
api.gen_output(random.randint(1, num))