import json
from promise import Promise

def add_task(task_id: str, path: str, launch_id: str):
    print(json.dumps({
        "type": "add_task",
        "task_id": task_id,
        "path": path,
        "launch_id": launch_id
    }))

def add_edge(from_id: str, to_id: str, launch_id: str):
    print(json.dumps({
        "type": "add_edge",
        "from_id": from_id,
        "to_id": to_id,
        "launch_id": launch_id
    }))

def add_promise(task_id: list[str], promise: Promise):
    print(json.dumps({
        "type": "add_promise",
        "task_id": task_id,
        "promise": promise
    }))