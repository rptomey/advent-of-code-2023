import sys
import re

def point_in_rectangle(rectangle, point):
    x1 = rectangle["x1"]
    y1 = rectangle["y1"]
    x2 = rectangle["x2"]
    y2 = rectangle["y2"]
    x = point["x"]
    y = point["y"]

    if x1 <= x <= x2:
        if y1 <= y <= y2:
            return True
        
    return False

def parse(file_name):
    plans = {
        "numbers": [],
        "symbols": []
    }

    with open(file_name) as f:
        row = 0
        for line in f:
            if line != "\n":
                col = 0
                clean_line = line.strip()
                number = {
                    "number": ""
                }
                for char in clean_line:
                    if re.match(r"\d", char):
                        if "start" not in number.keys():
                            number["start"] = col
                            number["row"] = row
                        number["number"] += char
                    elif not re.match(r"\d", char) and len(number["number"]) > 0:
                        number["end"] = col - 1
                        plans["numbers"].append(number)
                        number = {
                            "number": ""
                        }

                    if re.match(r"[^\d\.]", char):
                        symbol = {
                            "symbol": char,
                            "x": col,
                            "y": row
                        }
                        plans["symbols"].append(symbol)
                    col += 1
                if len(number["number"]) > 0:
                    number["end"] = col - 1
                    plans["numbers"].append(number)
                row += 1
    return plans

def part1(data):
    """Solve part 1."""
    total_value = 0

    numbers = data["numbers"]
    symbols = data["symbols"]

    for number in numbers:
        boundary = {
            "x1": number["start"] - 1,
            "y1": number["row"] - 1,
            "x2": number["end"] + 1,
            "y2": number["row"] + 1
        }
        for symbol in symbols:
            if point_in_rectangle(boundary, symbol):
                total_value += int(number["number"])
                break
    
    return total_value

def part2(data):
    """Solve part 2."""
    total_value = 0

    numbers = data["numbers"]
    symbols = data["symbols"]

    for number in numbers:
        boundary = {
            "x1": number["start"] - 1,
            "y1": number["row"] - 1,
            "x2": number["end"] + 1,
            "y2": number["row"] + 1
        }
        for symbol in symbols:
            if point_in_rectangle(boundary, symbol):
                if "parts" not in symbol.keys():
                    symbol["parts"] = [int(number["number"])]
                else:
                    symbol["parts"].append(int(number["number"]))

    for symbol in symbols:
        if "parts" in symbol.keys():
            if len(symbol["parts"]) == 2:
                gear_ratio = symbol["parts"][0] * symbol["parts"][1]
                total_value += gear_ratio

    return total_value

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