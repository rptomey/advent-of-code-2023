import sys
import re

def parse(file_name):
    data = {
        "seeds": [],
        "maps": {}
    }

    with open(file_name) as f:
        current_mapping = ""
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                if re.search(r"seeds\:", clean_line):
                    data["seeds"] = [int(seed) for seed in re.findall(r"\d+", clean_line)]
                elif re.search(r"map", clean_line):
                    current_mapping = clean_line.split()[0]
                    data["maps"][current_mapping.split("-")[0]] = {
                        "next": current_mapping.split("-")[2],
                        "ranges": []
                    }
                else:
                    numbers = [int(num) for num in re.findall(r"\d+", clean_line)]
                    mapping = {
                        "input_base": numbers[1],
                        "input_max": numbers[1] + numbers[2] - 1,
                        "adjustment": numbers[0] - numbers[1]
                    }
                    data["maps"][current_mapping.split("-")[0]]["ranges"].append(mapping)
    
    return data

def part1(data):
    """Solve part 1."""
    seeds = data["seeds"]
    maps = data["maps"]

    min_location = -1

    for seed in seeds:
        current_value = seed
        mapping_item = "seed"
        while mapping_item != "location":
            this_map = maps[mapping_item]
            next_map = this_map["next"]
            this_adjustment = 0
            for rng in this_map["ranges"]:
                if rng["input_base"] <= current_value <= rng["input_max"]:
                    this_adjustment = rng["adjustment"]
                    break
            current_value += this_adjustment
            mapping_item = next_map
        if min_location == -1 or current_value < min_location:
            min_location = current_value

    return min_location

def part2(data):
    seeds = data["seeds"]
    maps = data["maps"]
    seed_ranges = []
    min_location = -1
    while len(seeds) > 0:
        seed_min,seed_range = seeds.pop(0),seeds.pop(0)
        seed_ranges.append([seed_min,seed_min + seed_range - 1])
    
    for seed_range in seed_ranges:
        current_ranges = [seed_range]
        mapping_item = "seed"
        while mapping_item != "location":
            new_ranges = []
            this_map = maps[mapping_item]
            next_map = this_map["next"]
            unmapped_ranges = current_ranges
            while len(unmapped_ranges) > 0:
                range_to_map = unmapped_ranges.pop(0)
                map_count = len(this_map["ranges"])
                maps_checked = 0
                for current_mapping in this_map["ranges"]:
                    r_min = range_to_map[0]
                    r_max = range_to_map[1]
                    c_min = current_mapping["input_base"]
                    c_max = current_mapping["input_max"]
                    # break off any parts that don't fit into the mapping
                    if r_min < c_min and c_min <= r_max:
                        mapping_remainder = [r_min, c_min - 1]
                        unmapped_ranges.append(mapping_remainder)
                        r_min = c_min
                    if r_max > c_max and r_min <= c_max:
                        mapping_remainder = [c_max + 1, r_max]
                        unmapped_ranges.append(mapping_remainder)
                        r_max = c_max

                    if c_min <= r_min <= r_max <= c_max:
                        this_adjustment = current_mapping["adjustment"]
                        r_min += this_adjustment
                        r_max += this_adjustment
                        new_ranges.append([r_min,r_max])
                        break
                    else:
                        maps_checked += 1
                        if maps_checked == map_count:
                            new_ranges.append([r_min,r_max])
            current_ranges = new_ranges
            mapping_item = next_map
        for this_range in current_ranges:
            if min_location == -1 or this_range[0] < min_location:
                min_location = this_range[0]

    return min_location


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