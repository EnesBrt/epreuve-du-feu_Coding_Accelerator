# Trouver le plus grand carré

import sys
import random


def generate_plateau(x, y, density):
    plateau = []
    for i in range(y + 1):
        row = ""
        for j in range(x + 1):
            row += 'x' if random.randint(0, y) * 2 < density else '.'
        plateau.append(row)
    return plateau


arg_x = int(sys.argv[1])
arg_y = int(sys.argv[2])
arg_density = int(sys.argv[3])

if len(sys.argv) != 4:
    print("params needed: x y density")
    sys.exit()

print(f"{arg_y}.xo")
