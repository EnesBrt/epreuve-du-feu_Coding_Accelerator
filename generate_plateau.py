# Génerer un plateau

import random
import sys


def generate_plateau(x, y, density):
    plateau = []
    for i in range(y + 1):
        row = ""
        for j in range(x + 1):
            row += 'x' if random.randint(0, y) * 2 < density else '.'
        plateau.append(row)
    return plateau


if len(sys.argv) != 4:
    print("params needed: x y density")
    sys.exit()

arg_x = int(sys.argv[1])
arg_y = int(sys.argv[2])
arg_density = int(sys.argv[3])

plateau = generate_plateau(arg_x, arg_y, arg_density)

with open("plateau", "w") as f:
    f.write(f"{arg_y}.xo\n")
    for row in plateau:
        f.write(row + "\n")
