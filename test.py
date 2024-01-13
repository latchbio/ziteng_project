# import graphviz
# import time
# import tempfile

# g = graphviz.Digraph("Workflow", comment="Workflow")

# g.node("a", style="filled", color="grey")

# g.edge("a", "b")

# g.node("b", style="filled", color="black")
# g.node("b", shape="doubleellipse", style="filled", color="deepskyblue", xlabel="xlabel", label="label")

# # doctest_mark_exec()

# # g.render(directory="./", view=True)
# g.view()


# time.sleep(0.5)

# g.node("c", style="filled", color="orange")

# g.edge("a", "c")

# g.view()

import sys

# print(sys.argv[1])

# def test(names: list[str]):
#     for name in names:
#         print(name)

# test("a")
# test(["b", "c", "d"])

# a = ""

# print(a.split())

import json

l = json.loads(sys.argv[1])

for i in l:
    print(i)



# def modify(li: list):
#     li.append(1)
#     li.append(2)

# print(l)