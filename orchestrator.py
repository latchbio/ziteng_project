import asyncio
import graphviz
import json
import sys
from collections import defaultdict
from pathlib import Path
from promise import Promise
from task import Task, TaskStatus, TaskType

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

root_path = Path(__file__).parent


class Orchestrator:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}
        self.edges: dict[str, list[str]] = defaultdict(list)
        self.rev_edges: dict[str, list[str]] = defaultdict(list)
        self.iter = 0



    # add it to the orchestrator
    def add_task(self, task_id: str, path: str, input=None, launch_id: str=None):
        task = Task(task_id, path, input)

        self.tasks[task_id] = task

        if launch_id is not None:
            self.tasks[launch_id].increase_task()
            self.check_promises(launch_id)



    def add_edge(self, from_id: str, to_id: str, launch_id: str=None):
        self.edges[from_id].append(to_id)
        self.rev_edges[to_id].append(from_id)

        if launch_id is not None:
            self.tasks[launch_id].increase_edge()
            self.check_promises(launch_id)

    
    
    def remove_edge(self, from_id: str, to_id: str, launch_id: str=None):
        self.edges[from_id].remove(to_id)
        self.rev_edges[to_id].remove(from_id)

        if launch_id is not None:
            self.tasks[launch_id].decrease_edge()
            self.check_promises(launch_id)


    
    def add_promise(self, group: list[str], promise: Promise):
        if isinstance(group, list):
            for task_id in group:
                self.tasks[task_id].add_promise(promise)
                self.check_promises(task_id)
        elif isinstance(group, str):
            self.tasks[group].add_promise(promise)
            self.check_promises(group)

    

    def gen_output(self, task_id: str, output):
        t = self.tasks[task_id]
        t.output = output

    
    
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



    def refresh_status(self, task_id: str, pretask_id: str=None):
        t = self.tasks[task_id]

        if pretask_id is not None:
            pret = self.tasks[pretask_id]
            if pret.output is not None:
                t.inputs.append(pret.output)


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
            graph.node(task, fillcolor=self.tasks[task].status.value)
            branch = False
            map = False
            if self.tasks[task].type == TaskType.BRANCH and self.tasks[task].status != TaskStatus.SUCCESS:
                branch = True
                graph.node(task, shape="diamond", fillcolor=self.tasks[task].status.value, xlabel="branch")
                graph.node(task+"Branch1", shape="egg", fillcolor="grey")
                graph.edge(task, task+"Branch1")
                graph.node(task+"Branch2", shape="egg", fillcolor="grey")
                graph.edge(task, task+"Branch2")

            
            elif self.tasks[task].type == TaskType.MAP_TASK and self.tasks[task].status != TaskStatus.SUCCESS:
                map = True
                graph.node(task, shape="octagon", fillcolor=self.tasks[task].status.value, xlabel="map task")
                graph.node(task+"Map Tasks", shape="box3d", fillcolor="grey")
                graph.edge(task, task+"Map Tasks")

            for to in self.edges[task]:
                if branch:
                    graph.edge(task+"Branch1", to)
                    graph.edge(task+"Branch1", to)
                elif map:
                    graph.edge(task+"Map Tasks", to)
                else:
                    graph.edge(task, to)
        
        graph.render(directory="./graph/", view=True)


    def dynamic_display(self):
        graph = graphviz.Digraph()

        for task in self.tasks:
            graph.node(task, style="filled", color=self.tasks[task].status.value)
            branch = False
            map = False
            if self.tasks[task].type == TaskType.BRANCH and self.tasks[task].status != TaskStatus.SUCCESS:
                branch = True
                graph.node(task, shape="diamond", fillcolor=self.tasks[task].status.value, xlabel="branch")
                graph.node(task+"Branch1", shape="plain", fillcolor="grey", label="Branch1")
                graph.edge(task, task+"Branch1")
                graph.node(task+"Branch2", shape="plain", fillcolor="grey", label="Branch2")
                graph.edge(task, task+"Branch2")

            
            elif self.tasks[task].type == TaskType.MAP_TASK and self.tasks[task].status != TaskStatus.SUCCESS:
                map = True
                graph.node(task, shape="invhouse", fillcolor=self.tasks[task].status.value, xlabel="map task")
                graph.node(task+"Map Tasks", shape="box3d", fillcolor="grey", label="Map Tasks")
                graph.edge(task, task+"Map Tasks")

            for to in self.edges[task]:
                if branch:
                    graph.edge(task+"Branch1", to)
                    graph.edge(task+"Branch1", to)
                elif map:
                    graph.edge(task+"Map Tasks", to)
                else:
                    graph.edge(task, to)

        graph.render(directory="./graph/", filename=f"{self.iter}.gv", format="png")

        plt.imshow(mpimg.imread(f"./graph/{self.iter}.gv.png"))
        plt.show()


    # cold start
    async def cold_start(self):
        self.init_status()
        # self.graph_display("Workflow Start")

        while True:
            find = False
            
            for task_id in self.tasks:
                t = self.tasks[task_id]

                if t.status == TaskStatus.READY:
                    await self.execute(task_id)

                    find = True

                    for to_task_id in self.edges[task_id]:
                        self.refresh_status(to_task_id, task_id)
                    
                    self.dynamic_display()
                    
                    break
            
            if not find:
                print("finished!")
                # self.graph_display("Workflow Finished")
                break

            self.iter += 1


    # execute task with "task_id"
    async def execute(self, task_id):
        t = self.tasks[task_id]

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            t.path,
            json.dumps([task_id, self.edges[task_id]]), 
            json.dumps(t.inputs),
            env={"PYTHONPATH": root_path},
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        output = stdout.decode()
        messages = output.split('\n')

        for raw_msg in messages:
            if not raw_msg:
                break

            msg = json.loads(raw_msg)
            if msg['type'] == "add_task":
                self.add_task(msg['task_id'], msg['path'], msg['input'], task_id)
            elif msg['type'] == "add_edge":
                self.add_edge(msg['from_id'], msg['to_id'], task_id)
            elif msg['type'] == "remove_edge":
                self.remove_edge(msg['from_id'], msg['to_id'], task_id)
            elif msg['type'] == "add_promise":
                self.add_promise(msg['group'], msg['promise'])
            elif msg['type'] == "gen_output":
                self.gen_output(task_id, msg['output'])


        if await proc.wait() != 0:
            t.status = TaskStatus.FAILED
        
        t.status = TaskStatus.SUCCESS



    # resume from checkpoint
    def warm_start(self):
        return
    


orchestrator = Orchestrator()