import sys
import os
import pandas as pd

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = []

    with open(os.path.join(__location__, file_name)) as f:
        grid = []
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                row = list(clean_line)
                grid.append(row)
            elif len(grid) > 0:
                df = pd.DataFrame(grid)
                data.append(df)
                grid = []
        df = pd.DataFrame(grid)
        data.append(df)

    return data

def move_rocks_dataframe(df, direction):
    def move_up(col):
        for i in range(1, len(col)):
            if col[i] == 'O':
                for k in range(i - 1, -1, -1):
                    if col[k] == '#' or col[k] != '.':
                        break
                    col[k + 1], col[k] = col[k], col[k + 1]
        return col

    def move_down(col):
        for i in range(len(col) - 2, -1, -1):
            if col[i] == 'O':
                for k in range(i + 1, len(col)):
                    if col[k] == '#' or col[k] != '.':
                        break
                    col[k - 1], col[k] = col[k], col[k - 1]
        return col

    def move_left(row):
        return move_up(list(row))

    def move_right(row):
        return move_down(list(row))

    if direction == 0:
        df = df.apply(move_up, axis=0)
    elif direction == 2:
        df = df.apply(move_down, axis=0)
    elif direction == 1:
        df = df.apply(move_up, axis=1)
    elif direction == 3:
        df = df.apply(move_down, axis=1)

    return df

def calculate_load_for_row(row):
    rocks = (row == 'O').sum()  # Count occurrences of 'O' in the row
    weighting = len(row) - row.name  # Calculate the adjusted factor
    return rocks * weighting  # Multiply the count by the adjusted factor

def spin_df(df):
    rotated = df.T
    rotated = rotated[rotated.columns[::-1]].reset_index(drop=True)
    return rotated

def find_cycle_length(values):
    # Initialize two pointers: slow and fast
    slow = values[0]
    fast = values[0]

    # Move slow by one step and fast by two steps
    while True:
        slow = values[slow]
        fast = values[values[fast]]

        # If there's a cycle, the slow and fast pointers will meet
        if slow == fast:
            break

    # Count the number of steps until the pointers meet again
    count = 1
    fast = values[slow]
    while slow != fast:
        fast = values[fast]
        count += 1

    return count  # Return the length of the cycle

def part1(data):
    df = data[0].copy(deep=True)
    shifted_df = move_rocks_dataframe(df, 0)
    total_load = shifted_df.apply(calculate_load_for_row, axis=1).sum()
    return total_load

def part2(data):
    df = data[0].copy(deep=True)

    # Repeat until a loop is observed
    states = {}
    cycles = 1000000000
    for i in range(cycles):
        for j in range(4):
            df = move_rocks_dataframe(df, j)
        current_state = df.to_string()
        if current_state in states:
            loop_size = i - states[current_state]
            loop_start = states[current_state]
            break
        else:
            states[current_state] = i

    # Skip ahead to the end of the loop and finish the cycles
    steps = (cycles - (loop_start+1)) % loop_size
    for i in range(steps):
        for j in range(4):
            df = move_rocks_dataframe(df, j)

    load = df.apply(calculate_load_for_row, axis=1).sum()

    return load

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    #for path in ["example.txt"]:
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))