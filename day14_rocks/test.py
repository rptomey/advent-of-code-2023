grid = [
    ['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
    ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
    ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
    ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
    ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
    ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
    ['.', '.', '.', '.', '.', '.', '.', 'O', '.', '.'],
    ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
    ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.']
]

def move_zeros(grid):
    rows = len(grid)
    cols = len(grid[0])

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            # If the current cell contains '0', move it upwards
            if grid[i][j] == 'O':
                for k in range(i - 1, -1, -1):
                    # Check for conditions to stop movement
                    if grid[k][j] == '#' or grid[k][j] != '.':
                        break
                    # Swap '0' with '.' to move upwards
                    grid[k + 1][j], grid[k][j] = grid[k][j], grid[k + 1][j]

move_zeros(grid)

# Display the modified grid
for row in grid:
    print(' '.join(row))

#print(grid)
total = 0

grid.reverse()

for i in range(len(grid)):
    total += (grid[i].count("O")) * (i+1)

print(total)