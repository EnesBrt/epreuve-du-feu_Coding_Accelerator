# Trouver une forme

def read_file_to_2d_list(file_path):
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    return grid


board = read_file_to_2d_list('board.txt')
to_find = read_file_to_2d_list('to_find.txt')

print(board)
print(to_find)








