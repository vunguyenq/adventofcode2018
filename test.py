import datetime
from multiprocessing import Pool

exec_part = 2 # which part to execute
exec_test_case = 0 # 0 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test05.txt') as f:
    INPUT_TEST = f.read()

with open('input/input05.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def part1(input):
    polymer = list(input[0])
    while(True):
        i = 0
        reduces = []
        is_reducible = False
        # Mark all units to be reduced in current round
        while i in range(len(polymer) - 1):
            u1, u2 = polymer[i: i+2]
            if(abs(ord(u1) - ord(u2)) == 32):
                reduces.append(i)
                i += 2
                is_reducible = True
            else:
                i+=1
        # Reduce opposite adjacent units 
        if(is_reducible):
            for i, j in enumerate(reduces):
                del_index = j - i*2
                del polymer[del_index: del_index+2]
        else: # No more units to reduce
            break
    return len(polymer)

# Function to remove a unit (a/A) from polymer, reduce the polymer and return length after reduce
# To be executed in a single thread
def remove_unit(thread_input):
    polymer, c, i = thread_input
    removed_units = (c, chr(ord(c)-32))
    polymer_copy = [u for u in polymer.copy() if u not in removed_units]
    print(f"Pass {i} - removed unit {removed_units}. Polymer length without this unit: {len(polymer_copy)}. Reducing...")
    reduced_length = part1(["".join(polymer_copy)])
    return reduced_length

def part2(input):
    unique_chars = set(input[0].lower())
    polymer = list(input[0])
    min_lenght = len(polymer)
    print(f"Polymer lenght: {min_lenght}")
    print(f"Number of unit type: {len(unique_chars)}")

    # Prepare inputs for parallel threads
    thread_inputs = []
    for i,c in enumerate(unique_chars):
        thread_inputs.append((polymer, c, i))

    # Parallel process each unique character
    # https://docs.python.org/3/library/multiprocessing.html
    # Laptop has 8 logical processor (4 cores) => 8 threads at a time
    with Pool(8) as p:
        lengths_after_reduce = p.map(remove_unit, thread_inputs)
    return min(lengths_after_reduce)

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
