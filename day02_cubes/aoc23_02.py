import sys
import re

def parse(file_name):
    """Parse input"""
    games = []

    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                game = {
                    "game_number": int(clean_line.split(":")[0].split()[1]),
                    "pulls": [],
                    "maximums": {}
                }
                pulls = clean_line.split(":")[1].split(";")
                for pull in pulls:
                    pull_details = {}
                    dice_sets = pull.split(",")
                    for dice_set in dice_sets:
                        dice_count = int(re.search(r"\d+", dice_set).group(0))
                        dice_color = re.search(r"[^\d\s]+", dice_set).group(0)
                        pull_details[dice_color] = dice_count
                        if dice_color not in game["maximums"].keys() or dice_count > game["maximums"][dice_color]:
                            game["maximums"][dice_color] = dice_count
                    game["pulls"].append(pull)
                games.append(game)
    
    return games

def part1(data):
    """Solve part 1."""
    total_value = 0

    cube_limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    for game in data:
        if game["maximums"]["red"] <= cube_limits["red"]:
            if game["maximums"]["green"] <= cube_limits["green"]:
                if game["maximums"]["blue"] <= cube_limits["blue"]:
                    total_value += game["game_number"]

    return total_value

def part2(data):
    """Solve part 2."""
    total_power = 0
    
    for game in data:
        power =  game["maximums"]["red"] * game["maximums"]["green"] * game["maximums"]["blue"]
        total_power += power

    return total_power

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