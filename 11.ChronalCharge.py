import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test11.txt') as f:
    INPUT_TEST = f.read()

with open('input/input11.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return int(input.split('\n')[0])

def power_level_cell(x, y, S):
    return ((((x+10) * y + S) * (x+10)) % 1000) // 100 - 5

def part1(input):
    S = input
    grid = np.zeros([300,300], dtype=int)
    for i in range(300):
        for j in range(300):
            grid[i][j] = power_level_cell(i+1, j+1, S)
    
    max_pow, coor = 0, (0,0)
    for i in range(300-3):
        for j in range(300-3):
            total_pow = np.sum(grid[i:i+3, j:j+3])
            if max_pow < total_pow:
                max_pow = total_pow
                coor = (i+1, j+1)
    print(f"The largest 3x3 square's top-left is {coor} (with a total power of {max_pow}).")
    return ','.join(list(map(str,coor)))

def part2(input):
    S = input
    grid = np.zeros([300,300], dtype=int)
    for i in range(300):
        for j in range(300):
            grid[i][j] = power_level_cell(i+1, j+1, S)
    
    max_pow, coor, max_size = 0, (0,0), 0
    for size in range (1,300):
        for i in range(300 - size):
            for j in range(300 - size):
                total_pow = np.sum(grid[i:i+size, j:j+size])
                if max_pow < total_pow:
                    max_pow = total_pow
                    coor = (i+1, j+1)
                    max_size = size
        if size % 10 == 0: # Progress tracking
            print(f"Processing square size {size}...")

    print(f"The largest total square (with a total power of {max_pow}) is {max_size}x{max_size} and has a top-left corner of {coor})")
    return ','.join(list(map(str,coor)) + [str(max_size)])

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

