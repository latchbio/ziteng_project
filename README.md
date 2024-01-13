# Overview
Write a simple workflow orchestration engine:
1. Runs a DAG of tasks
2. Edge represent "runs-after" relationships. No inputs or outputs, only order of execution constraints
3. Tasks are `python` subprocesses
5. Only one task runs at a time

## Example:
DAG nodes: start, 1, 2, end
DAG edges: start -> 1, start -> 2, 2 -> end

Valid execution:
1. start
2. 1
3. 2
4. end

Alternative valid execution:
1. start
2. 2
3. end
4. 1

## Core Objective
Represent the static-dynamic workflow gradient in as much precision as possible

Fully static workflows are those for which the entire DAG is known without running any tasks

Fully dynamic workflows are those for which only the first node is known but additional edges/nodes can be defined when a node runs

Requirements:
1. Allow visualizing an accurate best possible as-of-this-moment DAG. Must accurately communicate all possible future execution paths (e.g. with a follow-up "wildcard" node)
2. Support fully static workflows using some kind of "Registration" phase
3. Support fully dynamic workflows by allowing a task to create nodes and edges arbitrarily while it runs
4. Support in-between workflows by allowing the workflow to "Promise" (during Registration or during Runtime) a constraint. The Orchestrator must ensure a Promise is never broken (and terminate workflows that break Promises)
5. All nodes/edges must be uniform. No DAG structure or execution pattern can be hard-coded in the Orchestrator. E.g. no hard-coded "branch" or "map-task" nodes/edges

Example Promises:
- No new nodes are created
- No new edges are created
- Only specific edges can be created
- Only specific nodes can be created
- No edges can be created starting at node A
- No edges can be created ending at node B
- etc.

You do not have to support any of the example promises

## Must-have Use Cases

1. Pre-determined workflow: DAG is always the same when the workflow finishes
2. Randomly branching workflow: DAG is always either A or B when the workflow finishes (decided randomly at Runtime)
3. Random map-task workflow: DAG is always A -> M* -> B where M repeats 0+ times (total number of repetitions decided randomly at Runtime)

## Implementation Suggestions
1. Use Python `asyncio`
2. Use SQLite to store state
3. Use GraphViz to visualize DAGs
4. Use JSON messages over stdio for task communication with workflow orchestrator -- do not need to design an more complicated RPC system / API

## Extras

1. Add strongly-typed task inputs/outputs
2. Allow branching based on a task input
3. Allow map-tasks to process a collection-type input and produce a collection-type output
4. Allow Promises related to "subgraphs" or graph "components". E.g. Promise that DAG is A -> X -> B where X is of form (N -> M) OR X is of form (J -> K)
5. Support running multiple tasks in parallel
6. Allow pausing and resuming a workflow execution (disable running the next avilable task)
7. Allow restarting a specific task (and all downstream tasks)
8. Allow waiting for user input in the Orchestrator (without having a task process sleep/block)
9. Support tasks that run Docker containers
10. Support cosmetic changes to the DAG (and related Promises) e.g. node color, edge label etc.
11. Support non-acyclic graphs