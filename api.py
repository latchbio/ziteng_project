import json
from promise import Promise

def add_task(task_id: str, path: str, input=None):
    print(json.dumps({
        "type": "add_task",
        "task_id": task_id,
        "path": path,
        "input": input
    }))

def add_edge(from_id: str, to_id: str):
    print(json.dumps({
        "type": "add_edge",
        "from_id": from_id,
        "to_id": to_id
    }))

def remove_edge(from_id: str, to_id: str):
        print(json.dumps({
        "type": "remove_edge",
        "from_id": from_id,
        "to_id": to_id
    }))

def add_promise(group: list[str], promise: Promise):
    print(json.dumps({
        "type": "add_promise",
        "group": group,
        "promise": promise
    }))

def gen_output(output):
    print(json.dumps({
        "type": "gen_output",
        "output": output
    }))