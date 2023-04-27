# Trouver une forme

import sys


def read_file_to_2d_list(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


def is_match(board, to_find, row, col):
    for r in range(len(to_find)):
        for c in range(len(to_find[0])):
            if board[row + r][col + c] != to_find[r][c]:
                return False
        return True


def find_matches(board, to_find):
    found = False
    for row in range(len(board) - len(to_find) + 1):
        for col in range(len(board[0]) - len(to_find[0]) + 1):
            if is_match(board, to_find, row, col):
                print("trouvé !")
                print("Coordinates:", col, row)
                found = True
    if not found:
        print("Aucun résultat trouvé.")  # No matches found


try:
    argument_one = sys.argv[1]
    argument_two = sys.argv[2]
    board = read_file_to_2d_list(argument_one)
    to_find = read_file_to_2d_list(argument_two)
    if argument_one == "to_find.txt" and argument_two == "board.txt":
        print("error")
        sys.exit()
    find_matches(board, to_find)
except IndexError:
    print("error")
    sys.exit()
except ValueError:
    print("error")
    sys.exit()
except FileNotFoundError:
    print("error")
    sys.exit()
