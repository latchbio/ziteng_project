import asyncio
import json
import sys
from collections import defaultdict
from pathlib import Path
from promise import Promise
from task import Task, TaskStatus


root_path = Path(__file__).parent


class Orchestrator:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}
        self.edges: dict[str, list[str]] = defaultdict(list)
        self.rev_edges: dict[str, list[str]] = defaultdict(list)



    # add it to the orchestrator
    def add_task(self, task_id: str, path: str, launch_id: str = None):
        task = Task(task_id, path)

        self.tasks[task_id] = task

        if launch_id is not None:
            self.tasks[launch_id].increase_task()
            self.check_promises(launch_id)



    def add_edge(self, from_id: str, to_id: str, launch_id: str = None):
        self.edges[from_id].append(to_id)
        self.rev_edges[to_id].append(from_id)

        if launch_id is not None:
            self.tasks[launch_id].increase_edge()
            self.check_promises(launch_id)


    
    def add_promise(self, group: list[str], promise: Promise):
        for task_id in group:
            self.tasks[task_id].add_promise(promise)
            self.check_promises(task_id)



    def init_status(self):
        for task_id in self.tasks:
            t = self.tasks[task_id]

            if t.status == TaskStatus.RUNNING:
                t.status = TaskStatus.READY

            elif t.status == TaskStatus.CREATED:
                self.refresh_status(task_id)



    def refresh_status(self, task_id: str):
        t = self.tasks[task_id]

        if t.status != TaskStatus.CREATED:
            return

        if len(self.rev_edges[task_id]) == 0:
            t.status = TaskStatus.READY
            return
        
        ready: bool = True

        for prior_task_id in self.rev_edges[task_id]:
            prior_task_status = self.tasks[prior_task_id].status
            if prior_task_status == TaskStatus.SUCCESS: # or prior_task_status == TaskStatus.FAILED:
                continue

            ready = False
        
        if ready:
            t.status = TaskStatus.READY



    def check_promises(self, task_id) -> bool:
        return self.tasks[task_id].check_promises()



    # cold start
    async def cold_start(self):
        self.init_status()

        while True:
            find = False
            
            for task_id in self.tasks:
                t = self.tasks[task_id]

                if t.status == TaskStatus.READY:
                    await self.execute(t)

                    find = True

                    for to_task_id in self.edges[task_id]:
                        self.refresh_status(to_task_id)
                    
                    break
            
            if not find:
                print("finished!")
                break


    # execute task with "task_id"
    async def execute(self, task_id):
        t = self.tasks[task_id]

        proc = await asyncio.create_subprocess_exec(
            [
                sys.executable,
                root_path + t.path, 
                task_id
            ], 
            env={"PYTHONPATH": root_path},
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if proc.wait() != 0:
            t.status = TaskStatus.FAILED
        
        for raw_msg in stdout:
            msg = json.loads(raw_msg.decode())
            if msg['type'] == "add_task":
                self.add_task(msg['task_id'], msg['path'], )
            if msg['type'] == "add_edge":
                self.add_edge(msg['from_id'], msg['to_id'])
        
        t.status = TaskStatus.SUCCESS



    # resume from checkpoint
    def warm_start(self):
        return
    


orchestrator = Orchestrator()