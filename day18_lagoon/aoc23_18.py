import sys
import os
import re
import copy

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    total_right = 0
    max_right = 0
    total_down = 0
    max_down = 0
    instructions = []

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                component = clean_line.split()
                direction = component[0]
                distance = int(component[1])
                match direction:
                    case "R":
                        total_right += distance
                    case "L":
                        total_right -= distance
                    case "D":
                        total_down += distance
                    case "U":
                        total_down -= distance
                if total_right > max_right:
                    max_right = total_right
                if total_down > max_down:
                    max_down = total_down
                color = re.search(r"[a-z0-9]{6}", component[2])[0]
                instruction = {
                    "direction": direction,
                    "distance": distance,
                    "color": color
                }
                instructions.append(instruction)

    return {
        "instructions": instructions,
        "width": max_right+1,
        "height": max_down+1
    }       

def shoelace_formula(boundary):
    positions = boundary
    a = 0
    b = 0
    for x in range(len(positions)):
        a += positions[x][1] * positions[(x+1) % len(positions)][0]
        b += positions[x][0] * positions[(x+1) % len(positions)][1]
    return int(abs(a-b)/2 - len(positions) /2 + 1)

def part1(data):
    grid = []
    for i in range(data["height"]):
        blank = {
            "char": ".",
            "color": None
        }
        blank_row = []
        for j in range(data["width"]):
            blank_row.append(copy.deepcopy(blank))
        grid.append(blank_row)

    # Pointer
    p_y = 0
    p_x = 0

    visited = []

    for line in data["instructions"]:
        for i in range(line["distance"]):
            match line["direction"]:
                case "R":
                    p_x += 1
                case "L":
                    p_x -= 1
                case "U":
                    p_y -= 1
                case "D":
                    p_y += 1
            visited.append((p_x,p_y))
            this_space = grid[p_y][p_x]
            this_space["char"] = "#"
            this_space["color"] = line["color"]

    return shoelace_formula(visited) + len(visited)

def part2(data):
    new_instructions = []
    distances = []

    for line in data["instructions"]:
        color = line["color"]
        distance = int(color[0:5], base=16)
        distances.append(distance)
        direction = int(color[-1])  # 0 means R, 1 means D, 2 means L, and 3 means U
        instruction = {
            "direction": direction,
            "distance": distance
        }
        new_instructions.append(instruction)

    # Pointer
    p_y = 0
    p_x = 0
    
    visited = []

    for line in new_instructions:
        for i in range(line["distance"]):
            match line["direction"]:
                case 0:
                    p_x += 1
                case 1:
                    p_y += 1
                case 2:
                    p_x -= 1
                case 3:
                    p_y -= 1
            visited.append((p_x,p_y))
    
    return shoelace_formula(visited) + len(visited)

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