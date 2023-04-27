# échauffement

import sys


def training(columns, rows):
    for row in range(rows):
        for col in range(columns):
            if (row, col) == (0, 0) or (row, col) == (0, columns - 1) or (row, col) == (rows - 1, 0) or (row, col) == (
                    rows - 1, columns - 1):
                print("O", end="")
            elif col == 0 or col == columns - 1:
                print("|", end="")
            elif row == 0 or row == rows - 1 and col != 0 and col != columns - 1:
                print("-", end="")
            else:
                print(" ", end="")
        print()


try:
    argument_one = int(sys.argv[1])
    argument_two = int(sys.argv[2])
    training(argument_one, argument_two)
except IndexError:
    print("error !")
    sys.exit()
except ValueError:
    print("error !")
    sys.exit()
except TypeError:
    print("error !")
    sys.exit()
