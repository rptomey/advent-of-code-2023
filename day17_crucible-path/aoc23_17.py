import sys
import os
import networkx as nx

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = []

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                row = [int(x) for x in list(clean_line)]
                data.append(row)

    return data

def find_minimal_heat_loss(grid):
    rows, cols = len(grid), len(grid[0])

    def is_valid(y, x):
        return 0 <= y < rows and 0 <= x < cols
    
    def is_backward(current_direction, new_direction):
        if current_direction == "r" and new_direction == "l":
            return True
        elif current_direction == "l" and new_direction == "r":
            return True
        elif current_direction == "u" and new_direction == "d":
            return True
        elif current_direction == "d" and new_direction == "u":
            return True
        else:
            return False

    def get_neighbors(this_node):
        neighbors = []
        y = this_node[0]
        x = this_node[1]
        direction = this_node[2]
        movement = this_node[3]

        d = ["u","d","l","r"]
        dm = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    
        for i in range(4): # Look in all 4 directions.
            if direction != d[i]: # If it's not a straight line, don't worry about movement.
                # But going backward is cheating.
                if not is_backward(direction, d[i]):
                    yn = y + dm[i][0]
                    xn = x + dm[i][1]
                    if is_valid(yn, xn):
                        neighbor = (yn, xn, d[i], 1)
                        if (this_node, neighbor) not in visited:
                            neighbors.append(neighbor)
            elif movement < 3: # If it is a straight line, we can't go this way if movement is 3.
                yn = y + dm[i][0]
                xn = x + dm[i][1]
                if is_valid(yn, xn):
                    neighbor = (yn, xn, d[i], movement+1)
                    if (this_node, neighbor) not in visited:
                        neighbors.append(neighbor)

        return neighbors

    G = nx.DiGraph()
    visited = set() # Make sure we aren't going back to nodes multiple times
    node_queue = [] # Each node we hit means we have to look at more nodes
    ends = set()

    # Do the steps manually for the first node before kicking off building the DiGraph.
    start = (0,0,"none",0)  # Starting node: (y,x,direction,movement)
    G.add_node(start)
    start_neighbors = get_neighbors(start)
    for neighbor in start_neighbors:
        visited.add((start, neighbor))
        node_queue.append(neighbor)
        G.add_node(neighbor)
        neighbor_y = neighbor[0]
        neighbor_x = neighbor[1]
        neighbor_weight = grid[neighbor_y][neighbor_x]
        G.add_edge(start, neighbor, weight=neighbor_weight)

    # Now do the same thing until the queue is empty.
    while node_queue:
        node = node_queue.pop(0)
        node_neighbors = get_neighbors(node)
        for neighbor in node_neighbors:
            visited.add((node, neighbor))
            node_queue.append(neighbor)
            G.add_node(neighbor)
            neighbor_y = neighbor[0]
            neighbor_x = neighbor[1]
            neighbor_weight = grid[neighbor_y][neighbor_x]
            G.add_edge(node, neighbor, weight=neighbor_weight)
            if neighbor_y == (rows - 1) and neighbor_x == (cols - 1):
                ends.add(neighbor)

    # At this point, we should have a complete DiGraph with all nodes and edges.
    # There may have been multiple ends reached, so we need to calculate all distances.
    shortest_weight = -1
    for end in ends:
        shortest_path = nx.shortest_path(G, source=start, target=end, weight="weight")
        weight = nx.path_weight(G,shortest_path,"weight")
        if shortest_weight == -1 or weight < shortest_weight:
            shortest_weight = weight

    return shortest_weight

def find_ultra_crucible_heat_loss(grid):
    rows, cols = len(grid), len(grid[0])

    def is_valid(y, x):
        return 0 <= y < rows and 0 <= x < cols
    
    def is_backward(current_direction, new_direction):
        if current_direction == "r" and new_direction == "l":
            return True
        elif current_direction == "l" and new_direction == "r":
            return True
        elif current_direction == "u" and new_direction == "d":
            return True
        elif current_direction == "d" and new_direction == "u":
            return True
        else:
            return False

    def get_neighbors(this_node):
        neighbors = []
        y = this_node[0]
        x = this_node[1]
        direction = this_node[2]
        movement = this_node[3]

        d = ["u","d","l","r"]
        dm = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    
        if movement < 4: # Not allowed to turn until movement is 4+
            di = d.index(direction)
            yn = y + dm[di][0]
            xn = x + dm[di][1]
            if is_valid(yn, xn):
                neighbor = (yn, xn, d[di], movement+1)
                neighbors.append(neighbor)
        else:
            for i in range(4): # Look in all 4 directions.
                if direction != d[i]: # If it's not a straight line, don't worry about movement.
                    # But going backward is cheating.
                    if not is_backward(direction, d[i]):
                        yn = y + dm[i][0]
                        xn = x + dm[i][1]
                        if is_valid(yn, xn):
                            neighbor = (yn, xn, d[i], 1)
                            if (this_node, neighbor) not in visited:
                                neighbors.append(neighbor)
                elif movement < 10: # If it is a straight line, we can't more than 10.
                    yn = y + dm[i][0]
                    xn = x + dm[i][1]
                    if is_valid(yn, xn):
                        neighbor = (yn, xn, d[i], movement+1)
                        if (this_node, neighbor) not in visited:
                            neighbors.append(neighbor)

        return neighbors

    G = nx.DiGraph()
    visited = set() # Make sure we aren't going back to nodes multiple times
    node_queue = [] # Each node we hit means we have to look at more nodes
    ends = set()

    # Do the steps manually for the first node before kicking off building the DiGraph.
    start = (0,0,"none",0)  # Starting node: (y,x,direction,movement)
    G.add_node(start)
    start_neighbors = [(0,1,"r",1),(1,0,"d",1)]
    for neighbor in start_neighbors:
        visited.add((start, neighbor))
        node_queue.append(neighbor)
        G.add_node(neighbor)
        neighbor_y = neighbor[0]
        neighbor_x = neighbor[1]
        neighbor_weight = grid[neighbor_y][neighbor_x]
        G.add_edge(start, neighbor, weight=neighbor_weight)

    # Now do the same thing until the queue is empty.
    while node_queue:
        node = node_queue.pop(0)
        node_neighbors = get_neighbors(node)
        for neighbor in node_neighbors:
            visited.add((node, neighbor))
            node_queue.append(neighbor)
            G.add_node(neighbor)
            neighbor_y = neighbor[0]
            neighbor_x = neighbor[1]
            neighbor_weight = grid[neighbor_y][neighbor_x]
            G.add_edge(node, neighbor, weight=neighbor_weight)
            if neighbor_y == (rows - 1) and neighbor_x == (cols - 1) and neighbor[3] >= 4:
                ends.add(neighbor)

    # At this point, we should have a complete DiGraph with all nodes and edges.
    # There may have been multiple ends reached, so we need to calculate all distances.
    shortest_weight = -1
    for end in ends:
        shortest_path = nx.shortest_path(G, source=start, target=end, weight="weight")
        weight = nx.path_weight(G,shortest_path,"weight")
        if shortest_weight == -1 or weight < shortest_weight:
            shortest_weight = weight

    return shortest_weight

def part1(data):
    return find_minimal_heat_loss(data)

def part2(data):
    return find_ultra_crucible_heat_loss(data)

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