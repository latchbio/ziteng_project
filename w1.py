import utils
import asyncio
from orchestrator import orchestrator
from promise import Promise


#       / d
# a - b - e
#   \ c - d1 - e
#       \ d2 /
#       \ d3 /
#       \ d4 /
#       \ d5 /

async def main():
    task_a = utils.generate_task_id("a")
    task_b = utils.generate_task_id("b")
    task_c = utils.generate_task_id("c")
    task_d = utils.generate_task_id("d")
    task_e1 = utils.generate_task_id("e")
    task_e2 = utils.generate_task_id("e")

    orchestrator.add_task(task_a, "tasks/a.py", input=5)
    orchestrator.add_task(task_b, "tasks/b.py")
    orchestrator.add_task(task_d, "tasks/d.py")
    orchestrator.add_task(task_e1, "tasks/e.py")
    orchestrator.add_task(task_c, "tasks/c.py")
    orchestrator.add_task(task_e2, "tasks/e.py")

    orchestrator.add_edge(task_a, task_b)
    orchestrator.add_edge(task_a, task_c)
    orchestrator.add_edge(task_b, task_d)
    orchestrator.add_edge(task_b, task_e1)
    orchestrator.add_edge(task_c, task_e2)

    orchestrator.add_promise(task_b, Promise.NO_NEW_TASK) # b - A or b - B
    orchestrator.add_promise(task_b, Promise.KEEP_ONE_EDGE)
    orchestrator.add_promise(task_c, Promise.FULL_NEW_TASK) # c - M* - e
    orchestrator.add_promise(task_c, Promise.FULL_NEW_EDGE)

    await orchestrator.cold_start()


if __name__ == "__main__":
    asyncio.run(main())