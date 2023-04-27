# Sudoku

import sys


def read_sudoku_file(file_path):
    grid = []
    with open(file_path, "r") as file:
        for line in file:
            grid.append([int(char) if char.isdigit() else 0 for char in line.strip()])
    return grid


def is_valid_number(grid, row, col, num):
    if num in grid[row]:
        return False

    for c in range(len(grid[0])):
        if num == grid[c][col]:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if num == grid[r][c]:
                return False
    return True


def sudoku_solver(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                for n in range(1, 10):
                    if is_valid_number(grid, r, c, n):
                        grid[r][c] = n
                        if sudoku_solver(grid):
                            return True
                        else:
                            grid[r][c] = 0
                return False
    return True


def show_result(grid):
    if sudoku_solver(grid):
        for row in grid:
            print(''.join(str(cell) for cell in row))
    else:
        print("Aucune solution trouvée")


try:
    argument = sys.argv[1]
    grid = read_sudoku_file(argument)
    show_result(grid)
except IndexError:
    print("error")
    sys.exit()
except ValueError:
    print("error")
    sys.exit()
except FileNotFoundError:
    print("error")
    sys.exit()
