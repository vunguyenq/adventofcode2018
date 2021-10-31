import datetime
import networkx as nx
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = -1 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test15.txt') as f:
    INPUT_TEST = f.read()

with open('input/input15.txt') as f:
    INPUT = f.read()   

# CONSTANTS
ADJACENTS = [np.array((-1,0)), np.array((0,-1)), np.array((0,1)), np.array((1,0))] # Adjacent cells in reading order

def parse_input(input):
    rows = input.split('\n')
    n_row, n_col = len(rows), len(rows[0])
    walls = np.zeros((n_row, n_col), dtype=np.byte)
    open_squares = nx.Graph()
    units = []
    for i,r in enumerate(rows):
        for j,c in enumerate(r):
            if c == '#':
                walls[i,j] = 1
            else:
                open_squares.add_node((i,j))
                for adjacent_node in [(i,j+1),(i,j-1),(i+1,j),(i-1,j)]:
                    if adjacent_node in open_squares.nodes:
                        open_squares.add_edge((i,j),adjacent_node)
                if(c in ['G','E']):
                    unit = Unit(c, np.array((i,j)))
                    units.append(unit)            
    return (walls, open_squares, units)

class Unit:
    def __init__(self,  type, initial_pos) -> None:
        self.pos = initial_pos
        self.type = type
        self.HP = 200
        self.AP = 3
        
    def next_action(self, open_squares, units):
        # check if enemies are alive
        no_more_enemies = True
        for u in units:
            if u.type != self.type and u.HP > 0:
                no_more_enemies = False
                break
        if(no_more_enemies):
            return 'No more enemies'

        move_result = self.move(open_squares, units)   

        # Scan adjacent cells in reading order to find enemy with lowest HP, if any
        min_hp = 201
        attacked_enemy = None
        for a in ADJACENTS:
            for u in units:
                if u.type == self.type: # Skip allies
                    continue
                if (u.pos == self.pos + a).all() and u.HP > 0: # Found 1 alive enemy
                    if(u.HP < min_hp):
                        attacked_enemy = u
                        min_hp = u.HP

        if (attacked_enemy is None and move_result):
            return 'Moved 1 step to nearest enemy'

        if (attacked_enemy is None and not move_result):
            return 'No possible move'

        enemy_HP = self.attack(attacked_enemy)
        if enemy_HP <= 0:
            #units.remove(attacked_enemy) # DO NOT remove killed unit immediately b/c it messes up the loop on units list. Instead mark unit as killed (HP <= 0) & remove at the end of the round
            #print(f"Unit {self.type} at {self.pos} has killed {attacked_enemy.type} at {attacked_enemy.pos}")
            return 'Killed 1 enemy unit'
        return 'Attacked 1 enemy unit'

    def move(self, open_squares, units):
        # 1 build up unit's own map: open_square + drop nodes that are occupied by an allied unit except for itself
        # No need to drop enemies b/c unit will find nearest enemies anyway
        self_vision = open_squares.copy()
        enemies = []
        for u in units:
            if u.type != self.type and u.HP > 0:
                enemies.append(u)
            elif (u.pos == self.pos).all() or u.HP <= 0: # do not remove self position and killed units (not yet removed b/c round may not finish) from graph
                continue
            else:
                self_vision.remove_node(tuple(u.pos))
    
        # 2 Find shortest_path_length to each enemies & find nearest enemies
        nearest_enemies = []
        enemy_distance = 9999
        for e in enemies:
            try:
                enemy_distance = nx.shortest_path_length(self_vision, source=tuple(self.pos), target=tuple(e.pos))  
            except nx.NetworkXNoPath: # No path to enemy, skip this enemy
                continue
            if enemy_distance == 1: # Enemy in range, no move
                return 0
            if len(nearest_enemies) == 0:
                nearest_enemies.append(e)
                min_distance = enemy_distance
            elif enemy_distance < min_distance:
                nearest_enemies = [e]
                min_distance = enemy_distance
            elif enemy_distance == min_distance:
                nearest_enemies.append(e)
            else:
                continue
        if len(nearest_enemies) == 0: # No possible path to any enemies
            return False
        
        for ad in ADJACENTS:
            new_pos = tuple(self.pos + np.array(ad)) 
            if new_pos in self_vision.nodes:
                for e in nearest_enemies:
                    new_distance = nx.shortest_path_length(self_vision, source=new_pos, target=tuple(e.pos))  
                    if new_distance == min_distance - 1:
                        self.pos = np.array(new_pos)
                        return True
        return None

    def attack(self, enemy):
        enemy.HP -= self.AP
        return enemy.HP


# Sort units by reading order
def sort_units1(units, walls):
    n_row, n_col = walls.shape
    sorted_units = []
    for i in range(n_row):
        for j in range(n_col):
            for u in units:
                if tuple(u.pos) == (i,j):
                    sorted_units.append(u)
                    if (len(sorted_units) == len(units)):
                        return(sorted_units)
                    else:
                        break
    return None

def sort_units(units):
    sorted_units = sorted(units, key = lambda x: (x.pos[0], x.pos[1]))
    return sorted_units

def print_map(walls, units):
    walls_print = np.copy(walls)
    for u in units:
        unit_type = 2 if u.type == 'G' else 3
        row,col = u.pos
        walls_print[row,col] = unit_type
    print('\n'.join([''.join([str(x) for x in row]) for row in walls_print]).replace('0','.').replace('1','#').replace('2','G').replace('3','E'))

def part1(input):
    walls, open_squares, units = input
    
    print_round_result = False # Set to True to print
    print_rounds = range(38)#[34,35,36,37,38]

    round = 0
    while(True):
        round += 1
        units = sort_units(units)
        for u in units:
            if (u.HP < 0): # If unit is killed but not yet removed => no action
                continue
            next_action = u.next_action(open_squares, units)
            if(next_action == 'No more enemies'):
                full_rounds = round - 1
                remaining_hp = sum([u.HP for u in units if u.HP > 0])
                return f"Full round: {full_rounds}. HP of all remaining units: {remaining_hp}. Result: {full_rounds * remaining_hp}"
            if(next_action == 'Killed 1 enemy unit'): # dead unit has been removed from units
                pass
            #print(u.type, u.pos, next_action) 
        # Collect killed units & remove from list:
        units = [u for u in units if u.HP > 0]
        #if print_round_result and round in print_rounds:
        # TODO: Check 1st test case https://www.reddit.com/r/adventofcode/comments/a6r6kg/2018_day_15_part_1_what_am_i_missing/. Nearest destination squares (in range of nearest targets) must be in reading orders
        if round == 1:
            print('')
            print(f"After {round} round(s):")
            print_map(walls, units)
            for u in units:
                print(u.type, u.pos, u.HP)
        
        # Progress tracking - real input only
        if exec_test_case == 0:
            print(f"Round {round}. Elf left: {len([u for u in units if u.type == 'E'])}; Goblins left: {len([u for u in units if u.type == 'G'])}")
    return 0

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
