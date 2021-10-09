import datetime
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test02.txt') as f:
    INPUT_TEST = f.read()

with open('input/input02.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def part1(input):
    box_2 = box_3 = 0
    for id in input:
        char_counts = set([])
        for c in set(id):
            char_counts.add(id.count(c))
            if 2 in char_counts and 3 in char_counts:
                break
        if 2 in char_counts:
            box_2 += 1
        if 3 in char_counts:
            box_3 += 1
    return box_2 * box_3

def part2(input):
    # Compute a dictionary: values = box ids, keys = sum ascii key of box ids
    box_dict = {}
    for id in input:
        key = sum([ord(c) for c in id])
        if key in box_dict:
            box_dict[key].append(id)
        else:
            box_dict[key] = [id]
    
    all_keys = list(box_dict.keys())
    all_keys.sort()

    for key in all_keys:
        # because there is only 1 letter different, ascii key of 2 correct box id must be within the range of +- 26
        # list is sorted => only need to look forward
        candidate_box_keys = [k for k in all_keys if k > key and k < key + 26]
        for candidate_key in candidate_box_keys:
            boxes_1 = box_dict[key]
            boxes_2 = box_dict[candidate_key]
            for b1 in boxes_1:
                for b2 in boxes_2:
                    diff = 0
                    for i in range(len(b1)):
                        if (b1[i] != b2 [i]):
                            diff += 1
                        if(diff > 1):
                            break
                    if(diff == 1):
                        return "".join([b1[i] for i in range(len(b1)) if b1[i] == b2 [i]])
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