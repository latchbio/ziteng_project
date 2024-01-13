import json
import sys

cur_task = json.loads(sys.argv[1])[0]
# cur_task = sys.argv[1][0]
inputs = sys.argv[2]
print(f"Task D is executing! Task Id: {cur_task}, Input: {inputs}", file=sys.stderr)