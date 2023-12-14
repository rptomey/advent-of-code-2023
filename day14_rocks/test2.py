import pandas as pd

# Your grid
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

def move_zeros_dataframe(grid):
    # Convert the grid into a DataFrame
    df = pd.DataFrame(grid)

    # Function to move '0' values upwards
    def move_up(col):
        for i in range(1, len(col)):
            if col[i] == 'O':
                for k in range(i - 1, -1, -1):
                    if col[k] == '#' or col[k] != '.':
                        break
                    col[k + 1], col[k] = col[k], col[k + 1]
        return col

    # Apply the move_up function to each column of the DataFrame
    df = df.apply(move_up, axis=0)

    return df

result_df = move_zeros_dataframe(grid)

# Display the modified DataFrame
print(result_df)

def count_zeros_multiply_adjusted_factor(row):
    zero_count = (row == 'O').sum()  # Count occurrences of 'O' in the row
    factor = len(row) - row.name  # Calculate the adjusted factor
    return zero_count * factor  # Multiply the count by the adjusted factor

# Apply the function to each row of the DataFrame
result = result_df.apply(count_zeros_multiply_adjusted_factor, axis=1)

# Calculate the total value produced across all rows
total_value = result.sum()

print("Result for each row multiplied by adjusted factor:")
print(result)
print("\nTotal value produced across all rows:", total_value)