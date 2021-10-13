import datetime
import networkx as nx
import matplotlib.pyplot as plt

exec_part = 2 # which part to execute
exec_test_case = 1 # 1 = test input; 0 = real puzzle input

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

def part2(input):
    result = 0
    return result

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