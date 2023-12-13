import sys
import os
from functools import lru_cache
from typing import Tuple

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = {
        "data": [],
        "big_data": []
    }

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                chunks = clean_line.split()
                pattern = chunks[0]
                groups = tuple([int(x) for x in chunks[1].split(",")])
                data["data"].append({
                    "pattern": pattern,
                    "groups": groups
                })
                data["big_data"].append({
                    "pattern": pattern + ("?" + pattern)*4,
                    "groups": groups*5
                })
    return data

# Copied and recommented recursion from here so I could understand it:
# https://github.com/shemetz/advent_of_code_2023/blob/main/day12.py
@lru_cache
def possibilities(pattern: str, groups: Tuple[int]):
    # Works left to right through both the pattern and the groups.
    if len(pattern) == 0:
        # If we're out of stuff to check and the groups have been satisfied,
        # this is a possible way to arrange the pattern
        return 1 if len(groups) == 0 else 0
    if pattern.startswith("."):
        # We know . isn't part of any groups, so get rid of it
        return possibilities(pattern.strip("."), groups)
    if pattern.startswith("?"):
        # Test how things shake out if the character is a . or a #
        a = possibilities(pattern.replace("?",".",1),groups)
        b = possibilities(pattern.replace("?","#",1),groups)
        return a + b
    if pattern.startswith("#"):
        # Non-matching cases that don't require more recursion first
        if len(groups) == 0:
            # We have a # that didn't get matched to any group
            return 0
        if len(pattern) < groups[0]:
            # We don't have enough characters to make the group
            return 0
        if any(c == "." for c in pattern[0:groups[0]]):
            # The group gets interrupted by an invalid character
            return 0
        if len(groups) > 1:
            if len(pattern) < groups[0] +1 or pattern[groups[0]] == "#":
                # Not enough pixels to have a . between two groups or too many # for the next group
                return 0
            # Group satistfied, so eliminate both it and the matching portion of the pattern
            return possibilities(pattern[groups[0]+1:],groups[1:])
        else:
            # Last group satisfied, so see if we've cleanly fit the pattern.
            return possibilities(pattern[groups[0]:], groups[1:])

def part1(data):
    total = 0
    for item in data["data"]:
        total += possibilities(item["pattern"],item["groups"])
    return total

def part2(data):
    total = 0
    for item in data["big_data"]:
        total += possibilities(item["pattern"],item["groups"])
    return total

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