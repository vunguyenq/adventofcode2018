import datetime
import pandas as pd
exec_part = 2 # which part to execute
exec_test_case = 0 # 1 = test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test04.txt') as f:
    INPUT_TEST = f.read()

with open('input/input04.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    df_log = df2 = pd.DataFrame(columns=['ts','event'])

    for entry in input.split('\n'):
        ts, event = entry.split("] ")
        ts = datetime.datetime.strptime(ts[1:], '%Y-%m-%d %H:%M')
        df_log = df_log.append({'ts':ts, 'event':event},ignore_index=True) 
    return df_log.sort_values(by=['ts'])

def part1(input):
    # Parse events
    df_log = input
    guards = {}
    for i, row in df_log.iterrows():
        ts, event = row['ts'], row['event']
        if ("begins shift" in event):
            current_guard = event.split()[1][1:]
            if current_guard not in guards:
                guards[current_guard] = []
        if ("falls asleep" in event):
            from_min = ts.minute
        if ("wakes up" in event):
            to_min = ts.minute
            guards[current_guard].append(range(from_min, to_min))
    
    # Find the guard who sleeps for the most minutes
    max_sleeping_time = 0
    selected_guard = 0
    for g in guards:
        sleeping_time = sum([len(r) for r in guards[g]])
        if (sleeping_time > max_sleeping_time):
            selected_guard = g
            max_sleeping_time = sleeping_time

    # List all minutes that selected guard sleeps
    minutes = []
    for r in guards[selected_guard]:
        minutes.extend(list(r)) 
    # Find most common minute    
    most_common_minute = max(set(minutes), key = minutes.count)
    return int(selected_guard) * most_common_minute

def part2(input):
    # Parse events
    df_log = input
    guard_minute = []
    for i, row in df_log.iterrows():
        ts, event = row['ts'], row['event']
        if ("begins shift" in event):
            current_guard = int(event.split()[1][1:])
        if ("falls asleep" in event):
            from_min = ts.minute
        if ("wakes up" in event):
            to_min = ts.minute
            for m in range(from_min, to_min):
                guard_minute.append((current_guard, m))
    
     # Find most common guard-minute    
    most_common_minute = max(set(guard_minute), key = guard_minute.count)
    print(f"Most common guard - sleeping minutes: {most_common_minute}")
    return most_common_minute[0] * most_common_minute[1]

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