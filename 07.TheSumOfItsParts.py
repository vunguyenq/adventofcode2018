import datetime
import networkx as nx
import matplotlib.pyplot as plt

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test07.txt') as f:
    INPUT_TEST = f.read()

with open('input/input07.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    steps = []
    for step in input.split('\n'):
        steps.append(tuple(step.replace('Step ','').replace('must be finished before step ','').replace(' can begin.','').split()))
    return steps

def part1(input):
    # Create graph
    G = nx.DiGraph()
    G.add_edges_from(input)

    # Visualize graph
    #plt.figure(figsize =(9, 9))
    #nx.draw_networkx(G)
    #plt.show()

    # Find first step (no prerequisite)
    node_queue = []
    for n in G.nodes:
        preds = list(G.predecessors(n))
        if len(preds) == 0:
            node_queue.append(n)
    node_queue.sort()

    executed_nodes = [] 
    while len(node_queue) > 0:
        executed_node = node_queue.pop(0)
        # Check if node has been executed befor (e.g closed loop)
        if executed_node in executed_nodes: 
            continue
        executed_nodes.append(executed_node)
        new_nodes = list(G.successors(executed_node))
        for n in new_nodes: 
            # Check if node is executable (i.e predecessor nodes have been executed)
            predecessors = list(G.predecessors(n))
            if set(predecessors).issubset(set(executed_nodes)): 
                node_queue.append(n)
        node_queue.sort()

    return ''.join(executed_nodes)

class Worker:
    def __init__(self):
        self.status = 'idle'
        self.active_task = None
        self.complete_at = None

    def update_status(self, sec):
        if sec == self.complete_at:
            self.status = 'idle'
            finished_task = self.active_task
            self.active_task = None
            self.complete_at = None
            return finished_task
        return self.status
    
    def start_working(self, task, sec):
        self.status = 'working'
        self.active_task = task
        #self.complete_at = sec + ord(task) - 1 - 64 # test
        self.complete_at = sec + 60 + ord(task) - 1 - 64 # prod

def part2(input):
    # Create graph
    G = nx.DiGraph()
    G.add_edges_from(input)

    # Find first step (no prerequisite)
    node_queue = []
    for n in G.nodes:
        preds = list(G.predecessors(n))
        if len(preds) == 0:
            node_queue.append(n)
    node_queue.sort()

    executed_nodes = [] 
    second = 0 # Global time
    workers = [Worker() for _ in range(6)] # Create a pool of 6 workers - PROD
    #workers = [Worker() for _ in range(2)] # Create a pool of 2 workers - TEST
    while len(executed_nodes) < len(G.nodes):
        # Assingn executable tasks to idle workers, if any
        idle_workers = [w for w in workers if w.status == 'idle']
        for worker in idle_workers:
            if len(node_queue) == 0:
                break
            executed_node = node_queue.pop(0)
            # Check if node has been executed befor (e.g closed loop)
            if executed_node in executed_nodes: 
                continue
            worker.start_working(executed_node, second)
        # Check if any worker finishes his work
        for worker in workers:
            report = worker.update_status(second)
            if report not in ('idle', 'working'): # worker reports a finished task
                executed_nodes.append(report)
                # Append new executable tasks to task queue
                new_nodes = list(G.successors(report))
                for n in new_nodes: 
                    # Check if node is executable (i.e all predecessor nodes have been executed)
                    predecessors = list(G.predecessors(n))
                    if set(predecessors).issubset(set(executed_nodes)): 
                        node_queue.append(n)
                node_queue.sort()
        
        # Update global time
        second += 1
    return second

if __name__ == "__main__":
    if(exec_test_case == 1):
        input = INPUT_TEST
    else:
        input = INPUT
    input = parse_input(input)

    start_time = datetime.datetime.now() 
    if (exec_part == 1):
        result = part1(input)
    else:
        result = part2(input)
    end_time = datetime.datetime.now() 
    print('Part {} time: {}'.format(exec_part, end_time - start_time))
    print('Part {} answer: {}'.format(exec_part, result))