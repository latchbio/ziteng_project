import utils
import asyncio
from orchestrator import orchestrator
from promise import Promise

async def main():
    task_a = utils.generate_task_id("a")
    task_b = utils.generate_task_id("b")
    task_c = utils.generate_task_id("c")
    task_d = utils.generate_task_id("d")

    orchestrator.add_task(task_a, "tasks/a.py")
    orchestrator.add_task(task_b, "tasks/b.py")
    orchestrator.add_task(task_c, "tasks/c.py")
    orchestrator.add_task(task_d, "tasks/d.py")

    orchestrator.add_edge(task_a, task_b)
    orchestrator.add_edge(task_a, task_c)
    orchestrator.add_edge(task_b, task_d)

    orchestrator.add_promise([task_b, task_c], Promise.DYNAMIC)
    orchestrator.add_promise([task_b], Promise.LIMITED_NEW_EDGE)

    await orchestrator.cold_start()

if __name__ == "__main__":
    asyncio.run(main())