import datetime
import numpy as np
from libraries.simpleframe import SimpleFrame
import libraries.simpleframe as sf

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input
VISUALIZE = False # Set to True to draw 
FRAME_RATE = 0.001
# Puzzle input
with open('input/input_test13.txt') as f:
    INPUT_TEST = f.read()

with open('input/input13.txt') as f:
    INPUT = f.read()   

# Shared constants
CELL_CODE = {
    ' ': 0,
    '-': 1,
    '<': 1,
    '>': 1,
    '|': 2,
    'v': 2,
    '^': 2,
    '/': 3,
    '\\': 4,
    '+': 5
}

CELL_CHAR = {
    0: ' ',
    1: '-',
    2: '|',
    3: '/',
    4: '\\',
    5: '+'
}

class Cart:
    def __init__(self, pos, direction) -> None:
        self.pos = np.array(pos)
        self.next_turn = 0
        if(direction == '>'):
            self.velocity = np.array((0,1))
        elif(direction == '<'):
            self.velocity = np.array((0,-1))
        elif(direction == '^'):
            self.velocity = np.array((-1,0))  
        else:
            self.velocity = np.array((1,0))

    def move(self, map):
        self.pos += self.velocity
        row,col = self.pos
        cell_val = map[row,col]    
        if CELL_CHAR[cell_val] == '/': 
            if self.velocity[0] == 0: # Moving horizontally
                self.turn('left')
            else: # Moving vertically
                self.turn('right')
        elif CELL_CHAR[cell_val] == '\\':
            if self.velocity[0] == 0: # Moving horizontally
                self.turn('right')
            else: # Moving vertically
                self.turn('left')
        elif CELL_CHAR[cell_val] == '+':
            turn_direction = ['left', 'straight', 'right'][self.next_turn]
            self.turn(turn_direction)
            self.next_turn = (self.next_turn + 1) % 3
    
    def turn(self, turn_direction):
        x, y = self.velocity
        if(turn_direction) == 'left':
            self.velocity = np.array((-y, x))
        elif (turn_direction) == 'right':
            self.velocity = np.array((y, -x))
        else: # Go straight
            pass

# Overide method draw of class SimpleFrame
class TrailMap(SimpleFrame):
    def draw(self, carts, trail_map, draw_result = False, result = {}):
        self.reset_background()
        # Draw map
        for row,col in np.ndindex(trail_map.shape):
            cell = trail_map[row,col]
            if CELL_CHAR[cell] == ' ':
                continue
            elif CELL_CHAR[cell] == '+':
                self.draw_tile((col,row), sf.BLUE)
            else:
                self.draw_tile((col,row), sf.RED)
        # Draw carts
        cart_positions = []
        for c in carts:
            self.draw_tile((c.pos[1],c.pos[0]), sf.GREEN)
            cart_positions.append(f"({str(c.pos[1])},{str(c.pos[0])})")
        text = ', '.join(cart_positions)
        self.display_text(f"Cart locations: {text}", 10, 10, color = sf.BLACK)
        if (draw_result):
            self.draw_tile((result['collision_loc'][1], result['collision_loc'][0]), sf.MAGENTA) # Collision point
            self.display_text(result['result_text'], 10, 40, color = sf.BLACK)
        self.refresh()
        self.check_closed()

def parse_input(input):
    rows = input.split('\n')
    trail_map = np.zeros((len(rows), len(rows[0])), dtype=np.int8)
    carts = []
    for row_no, row in enumerate(rows):
        row_code = []
        for col_no,c in enumerate(row):
            if c in ('>','<', '^', 'v'):
                carts.append(Cart((row_no, col_no),c))
            row_code.append(CELL_CODE[c])
        trail_map[row_no] = row_code
    return trail_map, carts

# Sort carts by their positions, top-left first
def sort_carts(carts):
    return sorted(carts, key=lambda h: (h.pos[0], h.pos[1]))
    
def part1(input):
    trail_map, carts = input
    if VISUALIZE:
    # Create canvas
        width, height = 1500, 1000
        tile_size = min(height // trail_map.shape[0], 20)
        trail_map_graphic = TrailMap(tile_size = tile_size, width = width, height = height, frame_rate = FRAME_RATE, left_margin = 0, top_margin = 100)
        trail_map_graphic.set_title("Day 10 par1 1")
        trail_map_graphic.set_font('Comic Sans MS', 18)
    # Move all carts in ticks until 1st collision 
    stop_move = False
    while(True): 
        carts = sort_carts(carts)
        for c in carts:
            #print(c.pos, c.velocity)
            if not(stop_move):
                c.move(trail_map) # Move each cart 1 step
                for c1 in carts: # Check collision with other carts
                    if(id(c1) == id(c)):
                        continue
                    if((c1.pos == c.pos).all()):
                        print(f"First collision location: {str(c.pos[1])},{str(c.pos[0])}")
                        stop_move = True
                        collision_loc = c.pos
                        break
        if not(stop_move):
            if VISUALIZE:
                trail_map_graphic.draw(carts, trail_map)
        else:
            result = {
                'result_text': f"First collision location: {str(c.pos[1])},{str(c.pos[0])}",
                'collision_loc': collision_loc
            }
            if VISUALIZE:
                trail_map_graphic.draw(carts, trail_map, draw_result = True, result=result)
            else:
                print(result['result_text'])
                return f"{str(collision_loc[1])},{str(collision_loc[0])}"
    return None

def part2(input):
    trail_map, carts = input
    # Create canvas
    if VISUALIZE:
        width, height = 1500, 1000
        tile_size = min(height // trail_map.shape[0], 20)
        trail_map_graphic = TrailMap(tile_size = tile_size, width = width, height = height, frame_rate = FRAME_RATE, left_margin = 0, top_margin = 100)
        trail_map_graphic.set_title("Day 10 par1 2")
        trail_map_graphic.set_font('Comic Sans MS', 18)
    # Move all carts in ticks until 1st collision 
    stop_move = False
    carts = sort_carts(carts)
    while(True): 
        removed_carts = [] 
        for c in carts:
            if id(c) in removed_carts:
                continue
            if not(stop_move):
                c.move(trail_map) # Move each cart 1 step
                for c1 in carts: # Check collision with other carts
                    if(id(c1) == id(c)):
                        continue
                    if((c1.pos == c.pos).all()):
                        print(f"Collision location: {str(c.pos[1])},{str(c.pos[0])}. Number of carts left: {len(carts) - 2}")
                        removed_carts.extend([id(c), id(c1)])
        if not(stop_move):
            carts = [c for c in carts if id(c) not in removed_carts]
            carts = sort_carts(carts)
            if(VISUALIZE):
                trail_map_graphic.draw(carts, trail_map)
            if(len(carts) == 1):
                stop_move = True
        else:
            result = {
                'result_text': f"Last cart location: {str(carts[0].pos[1])},{str(carts[0].pos[0])}",
                'collision_loc': carts[0].pos
            }
            if(VISUALIZE):
                trail_map_graphic.draw(carts, trail_map, draw_result = True, result=result)
            else:
                print(result['result_text'])
                return f"{str(carts[0].pos[1])},{str(carts[0].pos[0])}"
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

