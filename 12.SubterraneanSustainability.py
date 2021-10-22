import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test12.txt') as f:
    INPUT_TEST = f.read()

with open('input/input12.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    rules = []
    for row in input.split('\n'):
        if row == '':
            continue
        elif row[0] == 'i':
            initial_state = [int (i) for i in row.split(': ')[1].replace('#','1').replace('.','0')]
        else:
            rule_split = row.replace('#','1').replace('.','0').split(' => ')
            rules.append(([int(i) for i in rule_split[0]], int(rule_split[1])))
    return initial_state, rules

def part1(input):
    initial_state, rules = input
    n_gens = 20
    pots = np.zeros(len(initial_state) + n_gens*2*2, dtype=int) # each generation, space extend maximum 2 pots to each left, right direction 
    pots[n_gens*2 : n_gens*2 + len(initial_state)] = initial_state
    pots_sum = sum([i - n_gens*2 for i,p in enumerate(pots) if p == 1]) ## Check parttern for Part 2
    for n in range(n_gens):
        pots_next_gen = np.copy(pots)
        for i in range(len(pots) - 5): # Sliding window of length 5
            window = (pots[i:i+5])
            matched = False
            for (pattern, result) in rules: # Check if window matches any rule
                if((window == pattern).all()):
                    matched = True
                    break
            if (matched):
                pots_next_gen[i+2] = result
            else:
                pots_next_gen[i+2] = 0
        pots = np.copy(pots_next_gen) 
        ## Check parttern for Part 2
        new_pots_sum = sum([i - n_gens*2 for i,p in enumerate(pots) if p == 1])  
        print(f"Generation {n+1}. Sum of pot numbers with plant: {new_pots_sum}. Sum of last gen: {pots_sum}. Diff: {new_pots_sum - pots_sum}")     
        pots_sum = new_pots_sum
    result = sum([i - n_gens*2 for i,p in enumerate(pots) if p == 1])          
    return result

# Rerun Part 1 with n_gens = 300. Let sum(gen_n) = "sum of pot numbers with plan in gen n".
# Observe that from gen 100, sum(n) - sum(n-1) always == 62
# ...
# Generation 98. Sum of pot numbers with plant: 5569. Sum of last gen: 5509. Diff: 60
# Generation 99. Sum of pot numbers with plant: 5629. Sum of last gen: 5569. Diff: 60
# Generation 100. Sum of pot numbers with plant: 5691. Sum of last gen: 5629. Diff: 62
# Generation 101. Sum of pot numbers with plant: 5753. Sum of last gen: 5691. Diff: 62
# Generation 102. Sum of pot numbers with plant: 5815. Sum of last gen: 5753. Diff: 62
# Generation 103. Sum of pot numbers with plant: 5877. Sum of last gen: 5815. Diff: 62
# Generation 104. Sum of pot numbers with plant: 5939. Sum of last gen: 5877. Diff: 62
# ...
def part2(input):
    n = 50000000000
    result = 5691 + (n-100)*62
    return result

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

