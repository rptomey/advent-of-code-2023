import sys
import re
import math

def parse(file_name):
    instructions = []
    network = {}

    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                if re.search(r"=", clean_line):
                    connections = re.findall(r"\w{3}", clean_line)
                    node = {
                        "L": connections[1],
                        "R": connections[2]
                    }
                    network[connections[0]] = node
                else:
                    instructions = re.findall(r"\w", clean_line)
                    
    return {
        "instructions": instructions,
        "network": network
    }

def get_step_count(starting_node, end_node_type, network, instructions):
    instructions = instructions
    count = 0
    node = starting_node

    if end_node_type == "full": # Ends when characters are "ZZZ"
        while node != "ZZZ":
            direction = instructions.pop(0)
            instructions.append(direction)
            node = network[node][direction]
            count += 1
    elif end_node_type == "last": # Ends when last character is a "Z"
        while node[2] != "Z":
            direction = instructions.pop(0)
            instructions.append(direction)
            node = network[node][direction]
            count += 1

    return count

def part1(data):
    # Just following the map we're given is plenty fast, especially with only a single path to follow.
    return get_step_count("AAA", "full", data["network"], data["instructions"])

def part2(data):
    # Fortunately, the cycles repeat in such a way that we can use LCM to figure out when they'll sync up.
    starting_nodes = [x for x in data["network"].keys() if x[2] == "A"]
    counts = []
    for node in starting_nodes:
        count = get_step_count(node, "last", data["network"], data["instructions"])
        counts.append(count)
    return math.lcm(*counts)

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