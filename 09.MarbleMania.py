import datetime
from blist import *

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test09.txt') as f:
    INPUT_TEST = f.read()

with open('input/input09.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return list(map(int, input.replace('players; last marble is worth ','').replace(' points','').split()))

class MarbleCirle:
    def __init__(self, no_of_players):
        self.marble_list = blist([0])
        self.current_marble = 0
        self.current_player = 0
        self.no_of_players = no_of_players
        self.move_no = 0
        self.scores = [0] * no_of_players
        self.max_marble_point = 0
    
    # Return position of next n marbles from current_marble. +n => clockwise; -n => counter clockwise
    def get_next_n_marble_pos(self, n):
        pos = (self.current_marble + n) % len(self.marble_list)
        if pos < 0: # Convert negative list index to positive
            pos += len(self.marble_list)
        return (self.current_marble + n) % len(self.marble_list)

    def add_regular_marble(self, marble_value):
        self.current_marble = self.get_next_n_marble_pos(2)
        self.marble_list.insert(self.current_marble, marble_value)

    def take_turn(self):
        self.move_no += 1
        if (self.move_no % 23) == 0:
            self.current_marble = self.get_next_n_marble_pos(-7)
            removed_marble = self.marble_list.pop(self.current_marble)
            self.max_marble_point = self.move_no + removed_marble
            self.scores[self.current_player] += self.max_marble_point
        else:
            self.add_regular_marble(self.move_no)
        self.current_player = (self.current_player + 1) % self.no_of_players
    
    def print_circle(self):
        start_marble = min(self.marble_list)
        start_pos = self.marble_list.index(start_marble)
        print(f"Player: {self.current_player}. Last marble point: {self.max_marble_point}. Circle: {self.marble_list[start_pos:] + self.marble_list[0:start_pos]}")
            

# Changing from standard Python list to blist (http://stutzbachenterprises.com/blist/blist.html), performance of part 1 improves from 15s to 0.1s
def part1(input):
    no_players, last_marble_worth = input
    circle = MarbleCirle(no_players)
    for i in range(last_marble_worth + 1):
        circle.take_turn()
        #circle.print_circle()
        # Progress tracking
        if (i%10000) == 0:
            print(f"{i}/{last_marble_worth}")
    return max(circle.scores)

def part2(input):
    no_players, last_marble_worth = input
    circle = MarbleCirle(no_players)
    last_marble_worth = last_marble_worth*100
    for i in range(last_marble_worth + 1):
        circle.take_turn()
        # Progress tracking
        if (i%100000) == 0:
            print(f"{i}/{last_marble_worth}")
    return max(circle.scores)

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
