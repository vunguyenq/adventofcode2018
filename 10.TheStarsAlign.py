import datetime
import numpy as np
from libraries.simpleframe import SimpleFrame
import libraries.simpleframe as sf

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test10.txt') as f:
    INPUT_TEST = f.read()

with open('input/input10.txt') as f:
    INPUT = f.read()   

class Point:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity
    
    # Move point within 1 second
    def move_1_sec(self):
        self.pos += self.velocity
    
    # Reverse point within 1 second
    def move_back_1_sec(self):
        self.pos -= self.velocity

# Overide method draw of class SimpleFrame
class Sky(SimpleFrame):
    def draw(self, points, sec):
        self.reset_background()
        self.display_text(f"Second: {sec}", 300, 100, color = sf.BLACK)
        for p in points:
            self.draw_tile(p.pos, sf.BLUE)
        self.refresh()
        self.check_closed()

def parse_input(input):
    points = []
    for row in input.split('\n'):
        pos_str, vel_str = row.split('> ')
        pos = np.array(list(map(int, pos_str.replace('position=<','').split(', '))))
        vel = np.array(list(map(int, vel_str.replace('velocity=<','').replace('>','').split(', '))))
        points.append(Point(pos, vel))
    return points

def frame_size(points): # Return the size of frame limited by min_x, max_x, min_y, max_y 
    xs, ys = [p.pos[0] for p in points], [p.pos[1] for p in points]
    max_x, min_x = max(xs), min(xs)
    max_y, min_y = max(ys), min(ys)
    width, height = max_x - min_x, max_y - min_y
    return (width, height)

def part1(input):
    points = input
    #sky = Sky(tile_size = 10, frame_rate = 0.5, left_margin = 500, top_margin = 500) # Test case
    sky = Sky(tile_size = 5, frame_rate = 0.1, left_margin = -500, top_margin = -300) # Real puzzle
    sky.set_title("Day 10 par1 1")
    sky.set_font('Comic Sans MS', 30)

    sec = 1
    width, height = frame_size(points)
    for p in points:
        p.move_1_sec()
    stop_move = False

    while(True):
        new_width, new_height = frame_size(points)
        if new_width >= width and new_height >= height and not(stop_move):
            for p in points:
                p.move_back_1_sec()
            sec -= 1
            print(f"It takes {sec} seconds for the message to appear")
            stop_move = True

        if not stop_move:
            for p in points:
                p.move_1_sec()
            width, height = new_width, new_height
            sec += 1
        
        if(width < 300 and height < 300):
            sky.draw(points, sec)
        
    result = 0
    return result

def part2(input):
    part1(input)
    result = 0
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

