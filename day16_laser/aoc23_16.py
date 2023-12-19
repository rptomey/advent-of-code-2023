import sys
sys.setrecursionlimit(10000)
import os
import copy
from typing import Tuple

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = []

    with open(os.path.join(__location__, file_name)) as f:
        data = []
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                row = []
                for char in list(clean_line):
                    row.append({
                        "symbol": char,
                        "energized": False,
                        "lasers": []
                    })
                data.append(row)

    return data

def new_direction(current_direction, symbol):
    result = []
    match symbol:
        case "/":
            match current_direction:
                case "r":
                    result = ["u"]
                case "u":
                    result = ["r"]
                case "d":
                    result = ["l"]
                case "l":
                    result = ["d"]
        case "\\":
            match current_direction:
                case "r":
                    result = ["d"]
                case "d":
                    result = ["r"]
                case "u":
                    result = ["l"]
                case "l":
                    result = ["u"]
        case "-":
            match current_direction:
                case "d":
                    result = ["l","r"]
                case "u":
                    result = ["l","r"]
                case _:
                    result = [current_direction]
        case "|":
            match current_direction:
                case "r":
                    result = ["u","d"]
                case "l":
                    result = ["u","d"]
                case _:
                    result = [current_direction]
    return result

def get_next_yx(current_pos, direction):
    # The grid has 0,0 at its top-left, so down or right increase.
    curr_x = current_pos[1]
    curr_y = current_pos[0]

    match direction:
        case "u":
            curr_y -= 1
        case "d":
            curr_y += 1
        case "l":
            curr_x -= 1
        case "r":
            curr_x += 1
    
    return ([curr_y, curr_x])

#@lru_cache
def follow_laser(grid: Tuple[Tuple[dict]], current_pos: Tuple[int], direction: str):
    grid_h = len(grid)
    grid_w = len(grid[0])

    curr_x = current_pos[1]
    curr_y = current_pos[0]
    current_space = grid[curr_y][curr_x]
    current_space["energized"] = True

    if direction not in current_space["lasers"]:
        current_space["lasers"].append(direction)
        next_directions = [direction]
        symbol = current_space["symbol"]
        if symbol != ".":
            next_directions = new_direction(direction, symbol)
        for next_direction in next_directions:
            next_pos = get_next_yx(current_pos, next_direction)
            if -1 < next_pos[0] < grid_h:
                if -1 < next_pos[1] < grid_w:
                    follow_laser(grid, next_pos, next_direction)

def part1(data):
    grid = copy.deepcopy(data)
    start_pos = tuple([0,0])
    start_dir = "r"
    follow_laser(tuple(map(tuple, grid)), start_pos, start_dir)

    energy = 0
    for row in range(len(grid)):
        this_row = grid[row]
        for column in range(len(this_row)):
            if this_row[column]["energized"] == True:
                energy += 1
    return energy

def part2(data):
    grid_h = len(data)
    grid_w = len(data[0])
    max_energy = 0

    # Check top row
    for i in range(grid_w):
        grid = copy.deepcopy(data)
        start_pos = tuple([0,i])
        start_dir = "d"
        follow_laser(tuple(map(tuple, grid)), start_pos, start_dir)

        energy = 0
        for row in range(len(grid)):
            this_row = grid[row]
            for column in range(len(this_row)):
                if this_row[column]["energized"] == True:
                    energy += 1
        if energy > max_energy:
            max_energy = energy

    # Check left column
    for i in range(grid_h):
        grid = copy.deepcopy(data)
        start_pos = tuple([i,0])
        start_dir = "r"
        follow_laser(tuple(map(tuple, grid)), start_pos, start_dir)

        energy = 0
        for row in range(len(grid)):
            this_row = grid[row]
            for column in range(len(this_row)):
                if this_row[column]["energized"] == True:
                    energy += 1
        if energy > max_energy:
            max_energy = energy
    
    # Check bottom row
    for i in range(grid_w):
        grid = copy.deepcopy(data)
        start_pos = tuple([grid_h-1,i])
        start_dir = "u"
        follow_laser(tuple(map(tuple, grid)), start_pos, start_dir)

        energy = 0
        for row in range(len(grid)):
            this_row = grid[row]
            for column in range(len(this_row)):
                if this_row[column]["energized"] == True:
                    energy += 1
        if energy > max_energy:
            max_energy = energy

    # Check right column
    for i in range(grid_h):
        grid = copy.deepcopy(data)
        start_pos = tuple([i,grid_w-1])
        start_dir = "l"
        follow_laser(tuple(map(tuple, grid)), start_pos, start_dir)

        energy = 0
        for row in range(len(grid)):
            this_row = grid[row]
            for column in range(len(this_row)):
                if this_row[column]["energized"] == True:
                    energy += 1
        if energy > max_energy:
            max_energy = energy

    return max_energy

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