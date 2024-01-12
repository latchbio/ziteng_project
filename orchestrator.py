import asyncio
import graphviz
import json
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from promise import Promise
from task import Task, TaskStatus, TaskType


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


    
    def add_promise(self, group, promise):
        for task_id in group:
            self.tasks[task_id].add_promise(promise)
            self.check_promises(task_id)

    
    
    def check_promises(self, task_id):
        if not self.tasks[task_id].check_promises():
            # raise error
            exit(1)



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


    def graph_display(self, name: str):
        graph = graphviz.Digraph(name)
        
        for task in self.tasks:
            graph.node(task, style="filled", color=self.tasks[task].status.value)
            if self.tasks[task].type == TaskType.DYNAMIC:
                graph.node(task, fillcolor=self.tasks[task].status.value, xlabel="dynamic")

            for to in self.edges[task]:
                graph.edge(task, to)
        
        graph.render(directory="./graph/", view=True)


    def dynamic_display(self):
        graph = graphviz.Digraph()
        
        for task in self.tasks:
            graph.node(task, style="filled", color=self.tasks[task].status.value)
            if self.tasks[task].type == TaskType.DYNAMIC:
                graph.node(task, fillcolor=self.tasks[task].status.value, xlabel="dynamic")

            for to in self.edges[task]:
                graph.edge(task, to)

        graph.view(tempfile.mktemp('.gv'))


    # cold start
    async def cold_start(self):
        self.init_status()
        self.graph_display("Workflow Start")

        while True:
            find = False
            
            for task_id in self.tasks:
                t = self.tasks[task_id]

                if t.status == TaskStatus.READY:
                    await self.execute(task_id)

                    find = True

                    for to_task_id in self.edges[task_id]:
                        self.refresh_status(to_task_id)
                    
                    break
            
            if not find:
                print("finished!")
                self.graph_display("Workflow Finished")
                break


    # execute task with "task_id"
    async def execute(self, task_id):
        t = self.tasks[task_id]

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            t.path,
            task_id, 
            env={"PYTHONPATH": root_path},
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if await proc.wait() != 0:
            t.status = TaskStatus.FAILED
        
        for raw_msg in stdout:
            # print(raw_msg)
            msg = json.loads(raw_msg.decode())
            if msg['type'] == "add_task":
                self.add_task(msg['task_id'], msg['path'], task_id)
            if msg['type'] == "add_edge":
                self.add_edge(msg['from_id'], msg['to_id'], task_id)
            if msg['type'] == "add_promise":
                self.add_promise(msg['group'], msg['promise'])
        
        t.status = TaskStatus.SUCCESS
        # self.dynamic_display()



    # resume from checkpoint
    def warm_start(self):
        return
    


orchestrator = Orchestrator()