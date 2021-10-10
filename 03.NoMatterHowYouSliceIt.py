import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test03.txt') as f:
    INPUT_TEST = f.read()

with open('input/input03.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    claims = {}
    max_width = max_height = 0
    for claim in input.split('\n'):
        id, pos, size = "".join([c for c in claim if c not in ('#','@',':')]).split()
        pos = list(map(int, pos.split(",")))
        size = list(map(int, size.split("x")))
        max_width = max(max_width, pos[0] + size[0])
        max_height = max(max_height, pos[1] + size[1])
        claims[id] = {'pos': pos, 'size': size}
    return claims, (max_height, max_width)

def part1(input):
    claims, fabric_size = input
    fabric = np.zeros(fabric_size, dtype = int)
    for c in claims:
        pos = claims[c]['pos']
        size = claims[c]['size']
        fabric[pos[0] : pos[0] + size [0], pos[1] : pos[1] + size [1]] += 1
    return (fabric > 1).sum() 

def part2(input):
    claims, fabric_size = input
    fabric = np.zeros(fabric_size, dtype = int)
    # Make all claims
    for c in claims:
        pos = claims[c]['pos']
        size = claims[c]['size']
        fabric[pos[0] : pos[0] + size [0], pos[1] : pos[1] + size [1]] += 1
    # Check each claim to see if it overlaps with any other claims
    for c in claims:
        pos = claims[c]['pos']
        size = claims[c]['size']
        area = fabric[pos[0] : pos[0] + size [0], pos[1] : pos[1] + size [1]]
        if (area > 1).sum() == 0:
            return c
    return None

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