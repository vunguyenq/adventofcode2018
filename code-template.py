import datetime

exec_part = 1 # which part to execute
exec_test_case = 1 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/INPUT_TEST_FILE.txt') as f:
    INPUT_TEST = f.read()

with open('input/INPUT_REAL_FILE.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def part1(input):
    result = 0
    return result

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