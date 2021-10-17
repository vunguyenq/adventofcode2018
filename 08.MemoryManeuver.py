import datetime
from treelib import Node, Tree
import itertools

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input
ID_COUNTER = itertools.count() # Auto increment node IDs

# Puzzle input
with open('input/input_test08.txt') as f:
    INPUT_TEST = f.read()

with open('input/input08.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    input = list(map(int, input.split()))
    tree = Tree()
    build_tree(tree, input, 0)
    return tree

# Recursively create tree from input
def build_tree(tree, nbr_list, parent_node):
    if (len(nbr_list) == 0): # No more nodes to add
        return False
    child_count, meta_entries = nbr_list[:2]
    new_node_id = next(ID_COUNTER)
    # Create node
    if(len(tree) == 0): # root node:
        tree.create_node(new_node_id, new_node_id)
    elif child_count == 0: # Leaf nodes
        tree.create_node(new_node_id, new_node_id, parent = parent_node)
    else: # Intermediate nodes
        tree.create_node(new_node_id, new_node_id, parent = parent_node)
    # Create child node(s)
    offset = 0    
    for _ in range(child_count):            
        offset += build_tree(tree, nbr_list[2 + offset:], new_node_id)
    # Add data
    node = tree.get_node(new_node_id)
    node.data = {'metadata_entries': nbr_list[2 + offset: 2 + offset + meta_entries]}
    return meta_entries + 2 + offset # Return how many indexes have been used for this child node

# Recursively calculate node values - part 2
def node_values(tree, current_node):
    if current_node.is_leaf():
        current_node.data['value'] = sum(current_node.data['metadata_entries'])
        return 0
    child_nodes = tree.children(current_node.identifier)
    for node in child_nodes:
        node_values(tree, node)
    current_node_value = 0
    for i in current_node.data['metadata_entries']:
        if i <= len(child_nodes):
            current_node_value += child_nodes[i-1].data['value']
    current_node.data['value'] = current_node_value
    return 0

def part1(input):
    tree = input
    return sum([sum(node.data['metadata_entries']) for node in tree.all_nodes()])

def part2(input):
    tree = input
    node_values(tree, tree.get_node(tree.root))
    #tree.show()
    #for node in tree.all_nodes():
        #print(node)
    return tree.get_node(tree.root).data['value']

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