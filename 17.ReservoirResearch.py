import datetime
import numpy as np
import libraries.simpleframe as sf
from libraries.simpleframe import SimpleFrame
import collections

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test17.txt') as f:
    INPUT_TEST = f.read()

with open('input/input17.txt') as f:
    INPUT = f.read()   

class VisualizaGround(SimpleFrame):
    def draw(self, ground_scan, display_text):
        self.reset_background()
        self.display_text(display_text, 800, 10, color = sf.BLACK)
        n_row, n_col = ground_scan.shape
        for i in range(n_row):
            for j in range(n_col):
                if ground_scan[i,j] == 1:
                    self.draw_tile((j,i), sf.BLACK)
                elif ground_scan[i,j] == 2:
                    self.draw_tile((j,i), sf.BLUE)
                elif ground_scan[i,j] == 3:
                    self.draw_tile((j,i), sf.GREEN)
        self.refresh()
        self.check_closed()

def parse_input(input):
    clay_pos, x_flat, y_flat = [], [], []
    for row in input.split('\n'):
        coor1, coor2 = row.split(', ')   
        ax1, val = coor1.split('=')
        val = int(val)
        ax2, range_val = coor2.split('=')
        lower_bound, upper_bound = tuple(map(int, range_val.split('..')))
        range_val = range(lower_bound, upper_bound + 1)
        if ax1 == 'x':
            clay_pos.extend([(y, val) for y in range_val])
        else:
            clay_pos.extend([(val, x) for x in range_val])
        eval(f"{ax1}_flat.append(val)")
        eval(f"{ax2}_flat.extend({range_val})")

    x_min, x_max = min(x_flat), max(x_flat)    
    y_min, y_max = min(y_flat), max(y_flat)    
    ground_scan = np.zeros((y_max - y_min + 1, x_max - x_min + 3), dtype=int) # 0: sand, 1: clay, 2: running water, 3: still water
    for c in list(set(clay_pos)):
        row, col = c[0] - y_min, c[1] - x_min + 1
        ground_scan[row, col] = 1
    return (ground_scan, x_min, x_max, y_min, y_max)

def print_scan(ground_scan):
    print_map = {0 : '.', 1 : '#', 2 : '|', 3 : '~'}
    for row in ground_scan:
        print(''.join([print_map[i] for i in row]))

def part1(input):
    ground_scan, x_min, x_max, y_min, y_max = input
    ground_scan[0 , 500-x_min + 1] = 2 
    n_row, n_col = ground_scan.shape

    # Visualization
    #frame = VisualizaGround(tile_size = 1, frame_rate=0)
    #frame.set_title("Test draw")
    #frame.set_font('Comic Sans MS', 30)

    # Simulate water flow
    round_no = 0
    while(True):
        changed = False # indicator if any cell changes value in this pass
        for r in range(n_row-1):
            for c in range(n_col):
                if ground_scan[r,c] != 2: # Not running water
                    continue
                below_cell = ground_scan[r + 1, c]
                if below_cell == 0: # sand
                    ground_scan[r + 1, c] = 2
                elif below_cell == 2: # running water
                    pass
                else: # clay or still water
                    left_cell, right_cell = ground_scan[r, c-1], ground_scan[r, c+1]
                    if left_cell == 0: 
                        ground_scan[r, c-1] = 2
                        k = 1 
                        while(ground_scan[r, c-1-k] == 0 and ground_scan[r+1, c-1-k] in (1,3)):
                            ground_scan[r, c-1-k] = 2
                            k+=1
                        changed = True

                    elif left_cell == 1: # if running water in a bottom-left corner or a reservoir, start to scan to the right to find the right wall
                        level_full = True # indicator of whether water level containing the running water is full
                        for i in range(c, n_col):
                            if ground_scan[r, i] == 0:
                                level_full = False
                                break
                            if ground_scan[r, i] == 1: # hit right wall of reservoir
                                break
                        if level_full:
                            ground_scan[r, c:i] = 3
                            changed = True

                    if right_cell == 0:
                        ground_scan[r, c+1] = 2
                    elif right_cell == 1:
                        level_full = True # indicator of whether water level containing the running water is full
                        for i in range(0, c):
                            j = c - i
                            if ground_scan[r, j] == 0:
                                level_full = False
                                break
                            if ground_scan[r, j] == 1: # hit left wall of reservoir
                                break
                        if level_full:
                            ground_scan[r, j+1:c+1] = 3
                            changed = True
        
        # Visualize option 1: Print
        #print_scan(ground_scan)
        #print('')

        # Visualize option 2: Draw frame
        #frame.draw(ground_scan, f"Round: {round_no}")

        # progres tracking:
        if (round_no % 20 == 0):
            print(f"Scanning round {round_no}")
        round_no += 1
        if not(changed):
            break
    running_water, rested_water = np.count_nonzero(ground_scan == 2), np.count_nonzero(ground_scan == 3)  
    return f"Running water cells: {running_water}. Rested water cells: {rested_water}. Part 1 answer: {running_water + rested_water}. Part 2 answer: {rested_water}" 

# Answer already included in part 1 
def part2(input):
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

