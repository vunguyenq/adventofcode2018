import datetime
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test06.txt') as f:
    INPUT_TEST = f.read()

with open('input/input06.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return [tuple(map(int, s.split(", "))) for s in input.split('\n')]

def manhattan_dist(x, y):
    return abs(y[0] - x[0]) + abs(y[1] - x[1])

# Return maximum 2 points closest to a given point
def find_closest_points(given_point, points):
    first_point = points.pop()
    closest_points = [first_point]
    closest_dist = manhattan_dist(given_point, first_point)
    for point in points:
        dist = manhattan_dist(given_point, point)
        if dist < closest_dist:
            closest_dist = dist
            closest_points = [point]
        elif dist == closest_dist: 
            closest_points.append(point)
    return closest_points

def part1(input):
    # Give each point an id
    cor_ids = {}
    for i, c in enumerate(input):
        cor_ids[c] = i + 1
    # Find rectangular (x,y) boundaries of non-infinity areas
    lx, ly = zip(*input)
    min_x, max_x, min_y, max_y = min(lx), max(lx), min(ly), max(ly)
    # Model area within boundries by a numpy matrix
    np_area = np.zeros((max_x - min_x + 1, max_y - min_y + 1), dtype=int)
    # Scan each point within boundaries
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            current_cor = (x,y)
            matrix_cor = (x - min_x, y - min_y)
            closest_points = find_closest_points(current_cor, input.copy())
            if len(closest_points) > 1:  # more than 1 closest point to current coordinates
                pass
            else: 
                np_area[matrix_cor[0], matrix_cor[1]] = cor_ids[closest_points[0]]
    
    # Get cor_id appears in matrix edges:
    edge_cor_ids = []
    for edge in [np_area[0,:], np_area[1:,-1], np_area[-1,:-1], np_area[1:-1,0]]:
        edge_cor_ids.extend(edge.tolist()) 
    edge_cor_ids = set(edge_cor_ids)
    # Scan size of non-infinity areas
    area_sizes = []
    max_area_size = max_cor = max_cor_id = 0
    for cor in input:
        cor_id = cor_ids[cor]
        if(cor_id in edge_cor_ids): # Ignore coordinates that appear on at least 1 of 4 edges of area matrix
            continue
        else:
            area_size = np.count_nonzero(np_area == cor_id)
            if area_size > max_area_size:
                max_area_size = area_size
                max_cor = cor
                max_cor_id = cor_id
    print(f"Largest area size = {max_area_size} at coordinate{max_cor} (id: {max_cor_id}).")        
    return max_area_size

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