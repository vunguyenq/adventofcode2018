import datetime
import numpy as np
from itertools import product

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test18.txt') as f:
    INPUT_TEST = f.read()

with open('input/input18.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    rows = input.split('\n')
    n_row, n_col = len(rows), len(rows[0])
    np_area = np.zeros((n_row, n_col), dtype=int)
    for r, row in enumerate(rows):
        for c, char in enumerate(list(row)):
            if char == '#':
                np_area[r,c] = 1
            elif char == '|':
                np_area[r,c] = 2
            else:
                continue        
    return np_area

def scan_adjacents(pos, np_area):
    (r,c) = pos
    n_row, n_col = np_area.shape
    adjacent_locs = list(product([-1,0,1], repeat = 2))
    adjacent_locs.remove((0,0))
    adjacents = []
    for (r_incr,c_incr) in adjacent_locs:
        r_ad = r + r_incr
        c_ad = c + c_incr
        if r_ad not in range(n_row) or c_ad not in range (n_col):
            continue
        adjacents.append(np_area[r_ad,c_ad])        
    return adjacents

def process_minute(area):
    n_row, n_col = area.shape
    new_area = area.copy()
    for r in range(n_row):
        for c in range(n_col):
            current_acre = area[r,c]
            ajacents = scan_adjacents((r,c), area)
            if (current_acre == 0): # open acre '.'
                tree_count = len([i for i in ajacents if i == 2])
                if tree_count >= 3:
                    new_area[r,c] = 2
            elif (current_acre == 1): # lumberyard '#'
                tree_count = len([i for i in ajacents if i == 2])
                lumberyard_count = len([i for i in ajacents if i == 1])
                if not(tree_count >= 1 and lumberyard_count >=1):
                    new_area[r,c] = 0
            else: # tree '|'
                lumberyard_count = len([i for i in ajacents if i == 1])
                if lumberyard_count >= 3:
                    new_area[r,c] = 1
    return new_area

def part1(input):
    area = input
    n_row, n_col = area.shape
    for minute in range(10):
        area = process_minute(area)
    return np.count_nonzero(area == 1) * np.count_nonzero(area == 2)  

def part2(input):
    area = input
    seen_states = []
    minute = 0
    # Loop until find a previously seen state
    while(True):
        minute += 1
        seen_states.append(area)
        area  = process_minute(area)
        stop = False
        for prev_minute, prev_state in enumerate(seen_states):
            if ((prev_state == area).all()):
                print(f"Repeated state found at minute {minute}. Same state was previously seen at minute {prev_minute}")
                stop = True
                break
        if(stop):
            break
    
    # Run remaining minutes
    repeated_cycles = (1000000000 - prev_minute) // (minute - prev_minute) 
    remaining_mins = (1000000000 - prev_minute) % (minute - prev_minute)
    print(f"After 1000000000 minutes, {repeated_cycles} cycles of {minute - prev_minute} minutes each are repeated. Running {remaining_mins} more minutes.")
    for minute in range(remaining_mins):
        area = process_minute(area)
    return np.count_nonzero(area == 1) * np.count_nonzero(area == 2)  

if __name__ == "__main__":
    if(exec_test_case == 0):
        inputs = [INPUT]
    else:
        inputs = INPUT_TEST.split("\n#####INPUT_SEPERATOR#####\n")
    
    if exec_test_case > len(inputs):
        print(f"Test case {exec_test_case} does not exist")
        quit()
    for i, input_str in enumerate(inputs):
        if(exec_test_case == 0):
            print(f"Running real puzzle input...")
        elif (exec_test_case == -1):
            print(f"Running test case {i+1}/{len(inputs)}...")
        else:
            if (i+1 == exec_test_case):
                print(f"Running test case {i+1}/{len(inputs)}...")
            else:
                continue
            
        input = parse_input(input_str)
        start_time = datetime.datetime.now() 
        if (exec_part == 1):
            result = part1(input)
        else:
            result = part2(input)
        end_time = datetime.datetime.now() 

        print('Part {} time: {}'.format(exec_part, end_time - start_time))
        print('Part {} answer: {}\n'.format(exec_part, result))

