import sys
import re
import math

def quadratic(distance, time):
    """
    The distance traveled can be calculated by the following formula:
    (total_time - button_press_time) * button_press_time = distance
    OR
    (z - x) * x = y

    Simplified, this becomes:
    z * x - x^2 = y

    To figure out where y would equal 0 (i.e., the points where we meet the goal distance - or the roots),
    then we can change this into:
    x^2 - z * x + y = 0

    This type of equation can be run through the quadratic formula to give us the roots for x.
    """
    # Set the coefficients
    a = 1
    b = -time
    c = distance

    # Calculate the discriminant
    discriminant = b**2 - 4*a*c

    if discriminant >= 0:
        # Calculate the two solutions for x
        x1 = (-b - math.sqrt(discriminant)) / (2*a)
        x2 = (-b + math.sqrt(discriminant)) / (2*a)
        return [x1, x2]
    else:
        # No real roots
        return None
    
def roots_to_range(roots):
    option_range = []
        
    if roots[0].is_integer():
        option_range.append(int(roots[0] + 1))
    else:
        option_range.append(math.ceil(roots[0]))
    
    if roots[1].is_integer():
        option_range.append(int(roots[1] - 1))
    else:
        option_range.append(math.floor(roots[1]))

    return option_range

def parse(file_name):
    races = []
    times = []
    distances = []

    with open(file_name) as f:
        current_mapping = ""
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                if re.search(r"Time\:", clean_line):
                    times = [int(time) for time in re.findall(r"\d+", clean_line)]
                elif re.search(r"Distance\:", clean_line):
                    distances = [int(distance) for distance in re.findall(r"\d+", clean_line)]
    
    for i in range(len(times)):
        race = {
            "id": i,
            "time": times[i],
            "distance": distances[i]
        }
        races.append(race)

    return races

def part1(data):
    """Solve part 1."""
    options_per_race = []

    for race in data:
        distance = race["distance"]
        time = race["time"]
        roots = quadratic(distance,time)
        option_range = roots_to_range(roots)
        options_per_race.append(option_range[1]-option_range[0]+1)

    return math.prod(options_per_race)

def part2(data):
    time_str = ""
    distance_str = ""

    for race in data:
        time_str += str(race["time"])
        distance_str += str(race["distance"])

    time = int(time_str)
    distance = int(distance_str)

    roots = quadratic(distance,time)
    option_range = roots_to_range(roots)

    return option_range[1]-option_range[0]+1

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