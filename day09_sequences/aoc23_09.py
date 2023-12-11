import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

import re
import math

def parse(file_name):
    sequences = []

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                sequence = [int(x) for x in re.findall(r"\-?\d+", clean_line)]
                sequences.append(sequence)
                
    return sequences

def get_next(sequence):
    last_values = []
    last_values.append(sequence[-1])

    while not all(x==0 for x in sequence):
        temp = []
        for i in range(len(sequence)-1):
            temp.append(sequence[i+1]-sequence[i])
        last_values.append(temp[-1])
        sequence = temp

    return sum(last_values)

def part1(data):
    next_values = []
    for sequence in data:
        next_values.append(get_next(sequence))
        
    return sum(next_values)

def part2(data):
    prior_values = []
    for sequence in data:
        sequence.reverse()
        prior_values.append(get_next(sequence))

    return sum(prior_values)

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