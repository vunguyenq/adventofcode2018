import datetime

from libraries.opcode_computer import OpcodeComputer

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test16.txt') as f:
    INPUT_TEST = f.read()

with open('input/input16.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    rows = input.split('\n')
    i = 0
    part1_input = []
    part2_input = []
    while i < len(rows):
        row = rows[i]
        if row.startswith('Before'):
            before = list(map(int,rows[i].split('[')[1].replace(']','').split(', ')))
            instruction = rows[i+1]
            after = list(map(int,rows[i+2].split('[')[1].replace(']','').split(', ')))
            part1_input.append((before, instruction, after))
            i+=3 
        else:
            if len(row) > 0:
                part2_input.append(row) 
            i+=1
    return (part1_input, part2_input)

def part1(input):
    part1_input = input[0]
    instructions = ('addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr')
    sample_count = 0
    op = OpcodeComputer()
    possible_ins = {} 
    for sample in part1_input:
        before, instruction_code, after = sample
        matched_ins = 0
        for ins in instructions:
            code, params = instruction_code.split(' ',1)
            instruction_cmd = f"{ins} {params}"
            op.set_mem(before.copy())
            try:
                op.run_instruction(instruction_cmd)
                if op.mem == after:
                    matched_ins += 1
                    if ins in possible_ins:
                        possible_ins[ins].add(code)
                    else:
                        possible_ins[ins] = set([code])
            except:
                continue
        if(matched_ins >= 3):
            sample_count += 1
    return sample_count, possible_ins

def part2(input):
    _, part2_input = input
    possible_ins = part1(input)[1]
    # Work our instructions from codes
    while(True):
        # At each round, remove known code-instruction 
        next_round = False
        for cmd in possible_ins:
            for compare_cmd in possible_ins:
                if (cmd == compare_cmd or len(possible_ins[compare_cmd]) > 1 or len(possible_ins[cmd]) == 1):
                    continue
                possible_ins[cmd] = possible_ins[cmd] - possible_ins[compare_cmd]
                if len(possible_ins[cmd]) > 1:
                    next_round = True
        if not(next_round):
            break
    code_map = {possible_ins[cmd].pop():cmd for cmd in possible_ins} 
    
    # Run instructions
    op = OpcodeComputer()
    for ins in part2_input:
        ins_code, params = ins.split(' ', 1)
        instruction = f"{code_map[ins_code]} {params}"
        op.run_instruction(instruction)
    return op.mem[0]

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

