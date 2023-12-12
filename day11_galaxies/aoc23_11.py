import sys
import os
import copy

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def parse(file_name):
    space = {
        "galaxies": {},
        "size": {
            "w": 0,
            "h": 0
        }
    }
    index = 0

    with open(os.path.join(__location__, file_name)) as f:
        y = 0
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                x = 0
                for char in clean_line:
                    if char == "#":
                        galaxy = {
                            "id": index,
                            "pos": [x,y]
                        }
                        space["galaxies"][index] = galaxy
                        index += 1
                    x += 1
                if space["size"]["w"] == 0:
                    space["size"]["w"] = x
                y += 1
        space["size"]["h"] = y
                
    return space

def expand(space, amount):
    empty_col = set(range(space["size"]["w"]))
    empty_row = set(range(space["size"]["h"]))
    galaxy_queue = list(range(len(space["galaxies"])))

    while (len(empty_col) + len(empty_row)) != 0 and len(galaxy_queue) != 0:
        this_id = galaxy_queue.pop(0)
        this_galaxy = space["galaxies"][this_id]
        if this_galaxy["pos"][0] in empty_col:
            empty_col.remove(this_galaxy["pos"][0])
        
        if this_galaxy["pos"][1] in empty_row:
            empty_row.remove(this_galaxy["pos"][1])
    
    space["size"]["w"] += len(empty_col)
    space["size"]["h"] += len(empty_row)

    for galaxy_id in space["galaxies"].keys():
        this_galaxy = space["galaxies"][galaxy_id]
        x_adj = 0
        y_adj = 0
        for col in empty_col:
            if this_galaxy["pos"][0] > col:
                x_adj += amount
        this_galaxy["pos"][0] += x_adj
        for row in empty_row:
            if this_galaxy["pos"][1] > row:
                y_adj += amount
        this_galaxy["pos"][1] += y_adj

def manhattan_distance(p1,p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def part1(data):
    this_data = copy.deepcopy(data)
    expand(this_data,1)
    galaxies = this_data["galaxies"]

    distance_total = 0

    for id1 in galaxies.keys():
        for id2 in galaxies.keys():
            pos1 = galaxies[id1]["pos"]
            pos2 = galaxies[id2]["pos"]
            distance = manhattan_distance(pos1,pos2)
            distance_total += distance

    return int(distance_total / 2)


def part2(data):
    this_data = copy.deepcopy(data)
    expand(this_data,999999)
    galaxies = this_data["galaxies"]

    distance_total = 0

    for id1 in galaxies.keys():
        for id2 in galaxies.keys():
            pos1 = galaxies[id1]["pos"]
            pos2 = galaxies[id2]["pos"]
            distance = manhattan_distance(pos1,pos2)
            distance_total += distance

    return int(distance_total / 2)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
    #for path in ["example.txt"]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))