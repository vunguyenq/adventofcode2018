import datetime
from typing import SupportsComplex
from blist import *

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test14.txt') as f:
    INPUT_TEST = f.read()

with open('input/input14.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return int(input.split('\n')[0])

def part1(input):
    scoreboard = [3, 7]
    elf1_loc, elf2_loc = 0, 1
    while len(scoreboard) <= input + 10:
        new_recipes = list(map(int, list(str(scoreboard[elf1_loc] + scoreboard[elf2_loc]))))
        scoreboard.extend(new_recipes)
        elf1_loc = (elf1_loc + scoreboard[elf1_loc] + 1) % len(scoreboard)
        elf2_loc = (elf2_loc + scoreboard[elf2_loc] + 1) % len(scoreboard)
    return ''.join(list(map(str,scoreboard[input:input + 10])))

# Find 1st occurence of sublist in list. Only search from a specific location
def find_sublist(lst, sub_lst, search_index = 0):
    for i in range(search_index, len(lst) - len(sub_lst)):
        if lst[i:i+len(sub_lst)] == sub_lst:
            return i
    return -1

def part2(input):
    #input = 59414 # test case
    score_sequence = list(map(int, list(str(input))))
    scoreboard = [3, 7]
    elf1_loc, elf2_loc = 0, 1
    print(datetime.datetime.now(), f"Scoreboard length: {len(scoreboard)}") # progress tracking
    search_from = 0
    while True:
        new_recipes = list(map(int, list(str(scoreboard[elf1_loc] + scoreboard[elf2_loc]))))
        scoreboard.extend(new_recipes)
        elf1_loc = (elf1_loc + scoreboard[elf1_loc] + 1) % len(scoreboard)
        elf2_loc = (elf2_loc + scoreboard[elf2_loc] + 1) % len(scoreboard)
        first_occur = find_sublist(scoreboard, score_sequence, search_from)
        # progress tracking
        if len(scoreboard) % 100000 == 0:
            print(datetime.datetime.now(), f"Scoreboard length: {len(scoreboard)}. Search from index {search_from}")                
        if (first_occur >= 0):
            return first_occur
        search_from = len(scoreboard) - len(score_sequence) - len(new_recipes)
    return None

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

