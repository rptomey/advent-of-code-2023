import sys
import os
import pandas as pd
import numpy as np

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

def tupleize(df):
    return tuple(map(tuple, df.values))

def move_rocks(grid, direction):
    grid = np.array(grid)  # Convert the grid to a NumPy array

    if direction == 0:  # Move up
        for col in range(grid.shape[1]):
            for i in range(1, grid.shape[0]):
                if grid[i, col] == 'O':
                    for k in range(i - 1, -1, -1):
                        if grid[k, col] == '#' or grid[k, col] != '.':
                            break
                        grid[k + 1, col], grid[k, col] = grid[k, col], grid[k + 1, col]

    elif direction == 2:  # Move down
        for col in range(grid.shape[1]):
            for i in range(grid.shape[0] - 2, -1, -1):
                if grid[i, col] == 'O':
                    for k in range(i + 1, grid.shape[0]):
                        if grid[k, col] == '#' or grid[k, col] != '.':
                            break
                        grid[k - 1, col], grid[k, col] = grid[k, col], grid[k - 1, col]

    elif direction == 1:  # Move left
        for row in range(grid.shape[0]):
            for i in range(1, grid.shape[1]):
                if grid[row, i] == 'O':
                    for k in range(i - 1, -1, -1):
                        if grid[row, k] == '#' or grid[row, k] != '.':
                            break
                        grid[row, k + 1], grid[row, k] = grid[row, k], grid[row, k + 1]

    elif direction == 3:  # Move right
        for row in range(grid.shape[0]):
            for i in range(grid.shape[1] - 2, -1, -1):
                if grid[row, i] == 'O':
                    for k in range(i + 1, grid.shape[1]):
                        if grid[row, k] == '#' or grid[row, k] != '.':
                            break
                        grid[row, k - 1], grid[row, k] = grid[row, k], grid[row, k - 1]

    return grid.tolist()  # Convert back to a list of lists before returning

def part1(data):
    df = data[0].copy(deep=True)
    shifted_df = move_rocks_dataframe(df, 0)
    total_load = shifted_df.apply(calculate_load_for_row, axis=1).sum()
    return total_load

def part2(data):
    grid = [list(row) for row in data[0].values]  # Convert DataFrame to list of lists

    # Repeat until a loop is observed
    states = {}
    cycles = 1000000000
    for i in range(cycles):
        print(i)
        for j in range(4):
            grid = move_rocks(grid, j)
        current_state = tuple(map(tuple, grid))
        if current_state in states:
            loop_size = i - states[current_state]
            loop_start = states[current_state]
            break
        else:
            states[current_state] = i

    # Skip ahead to the end of the loop and finish the cycles
    steps = (cycles - loop_start) % loop_size
    for i in range(steps):
        for j in range(4):
            grid = move_rocks(grid, j)

    # Calculate the load
    load = sum(row.count('O') * (len(row) - i) for i, row in enumerate(grid))

    return load

def part2_slow(data):
    df = data[0].copy(deep=True)

    # Repeat until a loop is observed
    states = {}
    cycles = 1000000000
    for i in range(cycles):
        print(i)
        for j in range(4):
            df = move_rocks_dataframe(df, j)
        current_state = tupleize(df)
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