# Trouver le plus grand carré

import sys


# Fonction pour lire le plateau à partir d'un fichier
def read_plateau(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    plateau = [list(line.strip()) for line in lines[1:]]
    return plateau


# Fonction pour vérifier si un carré est valide (ne contient pas de 'x')
def is_valid_square(plateau, top_left_row, top_left_col, size):
    for n in range(top_left_row, top_left_row + size):
        for m in range(top_left_col, top_left_col + size):
            if plateau[n][m] == 'x':
                return False
    return True


# Fonction pour calculer le plus grand carré valide dans le plateau
def greater_square_calculator(plateau):
    if not plateau:
        return None, None, 0

    row = len(plateau)
    column = len(plateau[0])

    max_square_row = -1
    max_square_col = -1
    max_square_size = 0

    # Parcourir tous les carrés possibles dans l'ordre décroissant de leur taille
    for size in range(min(row, column), 0, -1):
        for n in range(row - size + 1):
            for m in range(column - size + 1):
                if is_valid_square(plateau, n, m, size):
                    max_square_row = n
                    max_square_col = m
                    max_square_size = size
                    return max_square_row, max_square_col, max_square_size

    return max_square_row, max_square_col, max_square_size


# Fonction pour marquer le plus grand carré valide avec des 'o'
def mark_greater_square(plateau, top_left_position, square_size):
    for n in range(top_left_position[0], top_left_position[0] + square_size):
        for m in range(top_left_position[1], top_left_position[1] + square_size):
            if 0 <= n < len(plateau) and 0 <= m < len(plateau[0]):
                if plateau[n][m] == '.':
                    plateau[n][m] = 'o'


# Fonction pour afficher le résultat (plateau avec le plus grand carré marqué)
def display_result(plateau, top_left_position, square_size):
    if top_left_position[0] is not None and top_left_position[1] is not None:
        mark_greater_square(plateau, top_left_position, square_size)

    for row in plateau:
        print("".join(row))

try:
    if len(sys.argv) != 2:
        print("params needed: plateau_filename")
        sys.exit()

    plateau_filename = sys.argv[1]
    plateau = read_plateau(plateau_filename)

    top_left_position_row, top_left_position_col, max_square_size = greater_square_calculator(plateau)
    top_left_position = (top_left_position_row, top_left_position_col)

    display_result(plateau, top_left_position, max_square_size)
except IndexError:
    print("error")
    sys.exit()
except ValueError:
    print("error")
    sys.exit()
except FileNotFoundError:
    print("error")
    sys.exit()

