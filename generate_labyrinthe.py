# Génerer un labyrinthe

import sys
import random


def generate_labyrinthe(height, width, chars):
    entry = random.randint(2, width - 3)
    exit1 = random.randint(2, width - 3)
    exit2_side = random.choice(["left", "right"])
    exit2 = random.randint(1, height - 2)

    with open("labyrinthe.map", "w") as f:
        f.write(f"{height}x{width}{chars}\n")

        for y in range(height):
            row = ""
            for x in range(width):
                if y == 0 and x == exit1:
                    row += chars[3]
                elif y == height - 1 and x == entry:
                    row += chars[2]
                elif (exit2_side == "left" and x == 0 and y == exit2) or (
                        exit2_side == "right" and x == width - 1 and y == exit2):
                    row += chars[4]
                elif 1 <= y < height - 1 and 1 <= x < width - 1:
                    if random.randint(0, 100) > 20:
                        row += ' '
                    else:
                        row += chars[0]
                else:
                    row += chars[0]
            f.write(row + "\n")


if len(sys.argv) < 4 or len(sys.argv[3]) < 4:
    print("params needed: height width characters")
else:
    height, width, chars = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    generate_labyrinthe(height, width, chars)
