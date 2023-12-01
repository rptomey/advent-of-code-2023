import sys
import re

def parse(file_name):
    """Parse input"""
    raw_input = []

    # First just get the stuff out of the file
    with open(file_name) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                raw_input.append(clean_line)
    
    return raw_input

number_words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def handle_digit(digit):
    if len(digit) == 1:
        return digit
    else:
        return str(number_words.index(digit))

def get_calibration_value(digits):
    first_digit = handle_digit(digits[0])
    last_digit = handle_digit(digits[-1])
    return int(first_digit + last_digit)

def part1(data):
    """Solve part 1."""
    total_value = 0
    for string in data:
        digits = re.findall(r"\d", string)
        if len(digits) >= 1:
            total_value += get_calibration_value(digits)

    return total_value

def part2(data):
    """Solve part 2."""
    total_value = 0

    for string in data:
        digits = re.findall(fr"(?=({'|'.join(number_words[1:])}|\d))", string)
        if len(digits) >= 1:
            total_value += get_calibration_value(digits)

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