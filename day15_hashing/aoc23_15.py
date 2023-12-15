import sys
import os
import pandas as pd
import numpy as np

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = {
        "original": [],
        "bins": {}
    }

    with open(os.path.join(__location__, file_name)) as f:
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                values = clean_line.split(",")
                for value in values:
                    val_len = len(value)
                    data["original"].append(value)
                    if val_len in data["bins"].keys():
                        data["bins"][val_len].append(value)
                    else:
                        data["bins"][val_len] = [value]

    return data

def hash_it(string,start_int):
    current_value = start_int
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value

def hashing(string,hash_map):
    hashed_value = 0
    s_len = len(string)

    # Check that we haven't already hashed it.
    if s_len in hash_map.keys():
        if string in hash_map[s_len]:
            return hash_map[s_len][string]
        
    # Work backwards through the string to see if we've hashed any portion of it.
    len_to_check = list(range(1,len(string)))
    len_to_check.sort(reverse=True)
    for i in len_to_check:
        sub_string = string[0:i]
        sub_len = len(sub_string)
        if sub_len in hash_map.keys():
            if sub_string in hash_map[sub_len].keys():
                # Found a value that was already hashed, so work back up to get each subset of the string into the hash_map.
                hashed_value = hash_map[sub_len][sub_string]
                character_difference = s_len - sub_len
                remaining_string = string[-character_difference:]
                for char in remaining_string:
                    sub_string = sub_string + char
                    new_sub_len = len(sub_string)
                    hashed_value = hash_it(char,hashed_value)
                    # Save hashes as we go.
                    if new_sub_len in hash_map.keys():
                        hash_map[new_sub_len][sub_string] = hashed_value
                    else:
                        hash_map[new_sub_len] = {}
                        hash_map[new_sub_len][sub_string] = hashed_value
    
    # At this point, if our hashed_value is 0, we didn't find anything to start with, so do the process for whole string.
    if hashed_value == 0:
        sub_string = ""
        for char in string:
            sub_string = sub_string + char
            sub_len = len(sub_string)
            hashed_value = hash_it(char,hashed_value)
            # Again, save as we go.
            if sub_len in hash_map.keys():
                hash_map[sub_len][sub_string] = hashed_value
            else:
                hash_map[sub_len] = {}
                hash_map[sub_len][sub_string] = hashed_value

    return hashed_value

def part1(data):
    bins = data["bins"]
    data["hashes"] = {}
    total = 0
    
    sizes = list(bins.keys())
    sizes.sort()

    for size in sizes:
        strings = bins[size]
        for string in strings:
            total += hashing(string, data["hashes"])

    return total

def part2(data):
    pass

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