import sys
import os
import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

pipe_key = {
    "|": ["north", "south"],
    "-": ["east", "west"],
    "L": ["north", "east"],
    "J": ["north", "west"],
    "7": ["south", "west"],
    "F": ["south", "east"]
}

opp = {
    "north": "south",
    "east": "west",
    "south": "north",
    "west": "east"
}

def get_neighbor(direction, pos):
    coord = [int(n) for n in pos.split(",")]
    match direction:
        case "north":
            coord[1] -= 1
        case "south":
            coord[1] += 1
        case "east":
            coord[0] += 1
        case "west":
            coord[0] -= 1
    return f"{coord[0]},{coord[1]}"

def parse(file_name):
    data = {}
    network = {}

    with open(os.path.join(__location__, file_name)) as f:
        y = 0
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                x = 0
                for char in clean_line:
                    if char == "S" or char in pipe_key.keys():
                        node = {
                            "c": char,
                            "pos": f"{x},{y}"
                        }

                        if char == "S":
                            data["start"] = f"{x},{y}"
                            node["open_to"]  = ["north", "south", "east","west"]
                        else:
                            node["open_to"] = pipe_key[char]

                        network[f"{x},{y}"] = node

                    x += 1
                y += 1

    # Check for valid neighbors
    for pos in network.keys():
        this_node = network[pos]
        neighbors = []
        for opening in this_node["open_to"]:
            neighbor = get_neighbor(opening, pos)
            if neighbor in network.keys():
                neighbors.append(neighbor)
        this_node["neighbors"] = neighbors
                
    data["network"] = network
    return data

def part1(data):
    start = data["start"]
    network = data["network"]

    G = nx.Graph().to_directed()

    for pos in network.keys():
        for neighbor in network[pos]["neighbors"]:
            G.add_edge(pos, neighbor)

    max_path = 0
    for neighbor in network[start]["neighbors"]:
        for cycle in nx.all_simple_paths(G, source=neighbor, target=start):
            if len(cycle) > max_path:
                max_path = len(cycle)
                data["max_cycle"] = cycle
    
    return max_path / 2

def shoelace_formula(boundary):
    nodes = []
    for node in boundary:
        arr = node.split(",")
        nodes.append([int(arr[0]),int(arr[1])])
    positions = nodes
    a = 0
    b = 0
    for x in range(len(positions)):
        a += positions[x][1] * positions[(x+1) % len(positions)][0]
        b += positions[x][0] * positions[(x+1) % len(positions)][1]
    return abs(a-b)/2 - len(positions) /2 + 1

def part2(data):
    return shoelace_formula(data["max_cycle"])

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = parse(path)
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))