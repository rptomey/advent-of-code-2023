import sys
import os
import re
import copy

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = {
        "flows": {},
        "parts": []
    }

    with open(os.path.join(__location__, file_name)) as f:
        read_type = "flows"
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                if read_type == "flows":
                    name = re.search(r"^[a-z]+", clean_line)[0]
                    steps = re.search(r"{(.+)}", clean_line).group(1).split(",")
                    data["flows"][name] = steps
                elif read_type == "parts":
                    raw_parts = re.search(r"{(.+)}", clean_line).group(1).split(",")
                    part = {}
                    for portion in raw_parts:
                        stat = portion.split("=")[0]
                        score = int(portion.split("=")[1])
                        part[stat] = score
                    data["parts"].append(part)
            else:
                read_type = "parts"
    
    return data

def follow_flow(part,flow_name):
    flow = workflows[flow_name]
    for step in flow:
        if ":" in step:
            rule = step.split(":")[0]
            result = step.split(":")[1]
            stat_name = re.search(r"^[xmas]", rule)[0]
            stat = part[stat_name]
            comp_value = int(re.search(r"[0-9]+", rule)[0])
            operator = re.search(r"\>|\<", rule)[0]
            test_result = False
            match operator:
                case ">":
                    if stat > comp_value:
                        test_result = True
                case "<":
                    if stat < comp_value:
                        test_result = True
            if test_result == True:
                if result == "A" or result == "R":
                    return result
                else:
                    return follow_flow(part,result)
        elif step == "A" or step == "R":
            return step
        else:
            return follow_flow(part, step)
        
def follow_flow_ranges(part, flow_name):
    flow = workflows[flow_name]
    for step in flow:
        if ":" in step:
            rule = step.split(":")[0]
            result = step.split(":")[1]
            stat_name = re.search(r"^[xmas]", rule)[0]
            stats = part[stat_name]
            comp_value = int(re.search(r"[0-9]+", rule)[0])
            operator = re.search(r"\>|\<", rule)[0]
            test_result = False
            match operator:
                case ">":
                    if min(stats) <= comp_value and max(stats) > comp_value:
                        new_sub_part = copy.deepcopy(part)
                        new_sub_part[stat_name] = [min(stats),comp_value]
                        parts_to_test.append(new_sub_part)
                        part[stat_name] = [comp_value+1, max(stats)]
                        test_result = True
                    elif min(stats) > comp_value:
                        test_result = True
                case "<":
                    if min(stats) < comp_value and max(stats) >= comp_value:
                        new_sub_part = copy.deepcopy(part)
                        new_sub_part[stat_name] = [comp_value,max(stats)]
                        parts_to_test.append(new_sub_part)
                        part[stat_name] = [min(stats),comp_value-1]
                        test_result = True
                    elif max(stats) < comp_value:
                        test_result = True
            if test_result == True:
                if result == "A" or result == "R":
                    return result
                else:
                    return follow_flow_ranges(part,result)
        elif step == "A" or step == "R":
            return step
        else:
            return follow_flow_ranges(part, step)


def part1(data):
    global workflows
    workflows = data["flows"]
    total = 0

    for part in data["parts"]:
        match follow_flow(part, "in"):
            case "A":
                total += sum(part.values())

    return total

def part2(data):
    global parts_to_test
    parts_to_test = []
    total = 0
    
    start = {
        "x": [1,4000],
        "m": [1,4000],
        "a": [1,4000],
        "s": [1,4000]
    }

    parts_to_test.append(start)

    while len(parts_to_test) > 0:
        next_part = parts_to_test.pop(0)
        match follow_flow_ranges(next_part, "in"):
            case "A":
                x = next_part["x"][1] - next_part["x"][0] + 1
                m = next_part["m"][1] - next_part["m"][0] + 1
                a = next_part["a"][1] - next_part["a"][0] + 1
                s = next_part["s"][1] - next_part["s"][0] + 1
                total += (x * m * a * s)
    
    return total


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