import sys
import os
import pandas as pd

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def parse(file_name):
    data = []

    with open(os.path.join(__location__, file_name)) as f:
        grid = []
        for line in f:
            if line != "\n":
                clean_line = line.strip()
                row = [0 if x == "." else 1 for x in list(clean_line)]
                grid.append(row)
            elif len(grid) > 0:
                df = pd.DataFrame(grid)
                data.append(df)
                grid = []
        df = pd.DataFrame(grid)
        data.append(df)

    return data

def is_reflection(df,start,end):
    size = df.shape[0]
    a = start
    b = end
    c = b + (b - a)
    if df.iloc[a:b].reset_index(drop=True).equals(df.iloc[b:c].iloc[::-1,:].reset_index(drop=True)):
        if a == 0 or c == size:
            return True
        else:
            return is_reflection(df,a-1,b)
    else:
        return False
    
def reflection_variance(df,a,b):
    size = df.shape[0]

    # The two columns/rows match
    if df.iloc[a].equals(df.iloc[b]):
        if a == 0 or b+1 == size:
            return 0
        else:
            return reflection_variance(df,a-1,b+1)
    else:
        if a == 0 or b+1 == size:
            #return 1
            return abs(df.iloc[a] - df.iloc[b]).sum()
        else:
            return abs(df.iloc[a] - df.iloc[b]).sum() + reflection_variance(df,a-1,b+1)
            #return 1 + reflection_variance(df,a-1,b+1)

def find_reflection_index(df,smudged):
    row_count = df.shape[0]
    for i in range(row_count-1):
        if smudged:
            if reflection_variance(df,i,i+1) == 1:
                return i
        else:
            if is_reflection(df,i,i+1):
                return i
    else:
        return None

def get_df_score(df,smudged):
    horizontal_reflection = find_reflection_index(df,smudged)
    if horizontal_reflection is not None:
        return (horizontal_reflection + 1) * 100
    else:
        vertical_reflection = find_reflection_index(df.T,smudged)
        if vertical_reflection is not None:
            return vertical_reflection + 1

def part1(data):
    total = 0
    for df in data:
        total += get_df_score(df, smudged=False)
    return total

def part2(data):
    total = 0
    for df in data:
        total += get_df_score(df, smudged=True)
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