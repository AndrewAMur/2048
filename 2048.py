import random
import os
import sys

def initialize_grid():
    grid = [[0] * 4 for _ in range(4)]
    add_random_tile(grid)
    add_random_tile(grid)
    return grid

def add_random_tile(grid):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 4

def print_grid(grid):
    os.system('clear')  # Use 'cls' for Windows
    for row in grid:
        print('\t'.join(str(cell) if cell != 0 else '.' for cell in row))
        print()

def move_left(grid):
    moved = False
    score_increment = 0
    for i in range(4):
        row = grid[i]
        new_row, merged, increment = merge_row(row)
        if row != new_row:
            moved = True
        grid[i] = new_row
        score_increment += increment
    return moved, score_increment

def move_right(grid):
    reversed_grid = [list(reversed(row)) for row in grid]
    moved, score_increment = move_left(reversed_grid)
    grid[:] = [list(reversed(row)) for row in reversed_grid]
    return moved, score_increment

def move_up(grid):
    transposed_grid = list(map(list, zip(*grid)))
    moved, score_increment = move_left(transposed_grid)
    grid[:] = list(map(list, zip(*transposed_grid)))
    return moved, score_increment

def move_down(grid):
    transposed_grid = list(map(list, zip(*grid)))
    moved, score_increment = move_right(transposed_grid)
    grid[:] = list(map(list, zip(*transposed_grid)))
    return moved, score_increment

def merge_row(row):
    new_row = [num for num in row if num != 0]
    merged_row = []
    score_increment = 0
    skip = False
    for i in range(len(new_row)):
        if skip:
            skip = False
            continue
        if i < len(new_row) - 1 and new_row[i] == new_row[i + 1]:
            merged_value = new_row[i] * 2
            merged_row.append(merged_value)
            score_increment += merged_value
            skip = True
        else:
            merged_row.append(new_row[i])
    merged_row += [0] * (len(row) - len(merged_row))
    return merged_row, merged_row != row, score_increment

def check_game_over(grid):
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                return False
            if c < 3 and grid[r][c] == grid[r][c + 1]:
                return False
            if r < 3 and grid[r][c] == grid[r + 1][c]:
                return False
    return True

def main():
    grid = initialize_grid()
    score = 0
    while True:
        print_grid(grid)
        print(f"Score: {score}")
        move = input("Move (WASD) or Q to quit: ").strip().upper()
        if move == 'W':
            moved, score_increment = move_up(grid)
        elif move == 'A':
            moved, score_increment = move_left(grid)
        elif move == 'S':
            moved, score_increment = move_down(grid)
        elif move == 'D':
            moved, score_increment = move_right(grid)
        elif move == 'Q':
            break
        else:
            print("Invalid input! Use W, A, S, D, or Q.")
            continue

        if moved:
            score += score_increment
            add_random_tile(grid)

        if check_game_over(grid):
            print("Game Over!")
            break

if __name__ == "__main__":
    main()

