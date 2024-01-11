import uuid

def generate_task_id(name: str) -> str:
    return "{}-{}".format(name, uuid.uuid4())