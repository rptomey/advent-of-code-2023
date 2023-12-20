import sys
import os
import re
import copy
import math
import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    G = nx.DiGraph()

    conjunction_modules = []

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                from_part = clean_line.split(" -> ")[0]
                from_name = re.search(r"[a-z]+", from_part)[0]
                from_type = re.search(r"[^a-z]", from_part)
                to_names = [n.strip() for n in clean_line.split(" -> ")[1].split(",")]
                for node_name in to_names:
                    G.add_edge(from_name,node_name)
                    G.nodes[node_name]["high_received"] = 0
                    G.nodes[node_name]["low_received"] = 0
                if from_type:
                    G.nodes[from_name]["type"] = from_type[0]
                    match from_type[0]:
                        case "%":
                            G.nodes[from_name]["on"] = False
                        case "&":
                            conjunction_modules.append(from_name)
                G.nodes[from_name]["high_sent"] = 0
                G.nodes[from_name]["low_sent"] = 0
    
    for node_name in conjunction_modules:
        input_nodes = G.predecessors(node_name)
        for in_name in input_nodes:
            G.nodes[node_name][f"last_{in_name}"] = "low"

    return G

def push_button(graph, pulse_queue):
    for target_node in graph.successors("broadcaster"):
        graph.nodes["broadcaster"]["low_sent"] += 1
        send_pulse(graph, "low", "broadcaster", target_node, pulse_queue, False)

def send_pulse(graph, pulse_type, sender, receiver, pulse_queue, from_queue):
    if from_queue:
        graph.nodes[receiver][f"{pulse_type}_received"] += 1
        if "type" in graph.nodes[receiver].keys():
            node_type = graph.nodes[receiver]["type"]
            match node_type:
                case "%":
                    if pulse_type == "low":
                        graph.nodes[receiver]["on"] = not graph.nodes[receiver]["on"]
                        next_pulse = "high" if graph.nodes[receiver]["on"] else "low"
                        for target_node in graph.successors(receiver):
                            graph.nodes[receiver][f"{next_pulse}_sent"] += 1
                            send_pulse(graph, next_pulse, receiver, target_node, pulse_queue, False)
                case "&":
                    graph.nodes[receiver][f"last_{sender}"] = pulse_type
                    # Only sends a low pulse if all senders are high
                    next_pulse = "low" if list(graph.nodes[receiver].values()).count("low") == 0 else "high"
                    for target_node in graph.successors(receiver):
                        graph.nodes[receiver][f"{next_pulse}_sent"] += 1
                        send_pulse(graph, next_pulse, receiver, target_node, pulse_queue, False)
    else:
        pulse_queue.append([graph, pulse_type, sender, receiver, pulse_queue, True])

def part1(data):
    graph = copy.deepcopy(data)
    high_sent = 0
    low_sent = 0

    for i in range(1000):
        pulse_queue = []
        push_button(graph, pulse_queue)
        low_sent += 1
        while pulse_queue:
            next_pulse = pulse_queue.pop(0)
            send_pulse(*next_pulse)
    
    for node in graph.nodes():
        if "high_sent" in graph.nodes[node].keys():
            high_sent += graph.nodes[node]["high_sent"]
        if "low_sent" in graph.nodes[node].keys():
            low_sent += graph.nodes[node]["low_sent"]
    
    return low_sent * high_sent

def part2(data):
    graph = copy.deepcopy(data)
    button_presses = 0
    # zh will send a low pulse to rx if all 4 of its incoming nodes are aligned on sending a high pulse
    # lcm will give us when rx gets its low pulse
    zh_xc = -1
    zh_th = -1
    zh_pd = -1
    zh_bp = -1

    while zh_xc == -1 or zh_th == -1 or zh_pd == -1 or zh_bp == -1:
        pulse_queue = []
        push_button(graph, pulse_queue)
        button_presses += 1
        while pulse_queue:
            next_pulse = pulse_queue.pop(0)
            send_pulse(*next_pulse)
            if graph.nodes["zh"]["last_xc"] == "high" and zh_xc == -1:
                zh_xc = button_presses
            if graph.nodes["zh"]["last_th"] == "high" and zh_th == -1:
                zh_th = button_presses
            if graph.nodes["zh"]["last_pd"] == "high" and zh_pd == -1:
                zh_pd = button_presses
            if graph.nodes["zh"]["last_bp"] == "high" and zh_bp == -1:
                zh_bp = button_presses
    
    return math.lcm(zh_xc, zh_th, zh_pd, zh_bp)

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