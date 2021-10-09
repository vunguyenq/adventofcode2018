import datetime
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test01.txt') as f:
    INPUT_TEST = f.read()

with open('input/input01.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def part1(input):
    return sum([int(i) for i in input])

def part2(input):
    seen_freqs = set([])
    freq = 0
    input = [int(i) for i in input]
    while(True):
        for i in input:
            freq += i
            if freq in seen_freqs:
                return freq
            seen_freqs.add(freq)    
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