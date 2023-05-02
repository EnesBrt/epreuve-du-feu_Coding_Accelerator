# Labyrinthe

def read_labyrinthe_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    labyinthe = [list(line.strip()) for line in lines[1:]]
    return labyinthe


def find_start_and_exit(labyrinthe):
    for row in range(len(labyrinthe)):
        for col in range(len(labyrinthe[0])):
            if labyrinthe[row][col] == '1':
                entry = (row, col)
            elif labyrinthe[row][col] == '2':
                output = (row, col)
    return entry, output


def create_graph_from_labyrinthe(labyrinthe):
    graph = {}
    rows = len(labyrinthe)
    cols = len(labyrinthe[0])

    for row in range(rows):
        for col in range(cols):
            if labyrinthe[row][col] in [' ', '1', '2']:
                node = (row, col)
                graph[node] = []

                # Liste des voisins possibles: haut, bas, gauche, droite
                neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                for neighbor in neighbors:
                    n_row, n_col = neighbor
                    if 0 <= n_row < rows and 0 <= n_col < cols and labyrinthe[n_row][n_col] in [' ', '1', '2']:
                        graph[node].append(neighbor)
    return graph


def manhattan_distance(current_node, goal_node):
    current_node_x = current_node.x
    current_node_y = current_node.y

    goal_node_x = goal_node.x
    goal_node_y = goal_node.y

    diff_x = abs(current_node_x - goal_node_x)
    diff_y = abs(current_node_y - goal_node_y)

    manhattan_distance = diff_x + diff_y

    return manhattan_distance


def a_star_algorithm(graph, start_node, goal_node, heuristic_func):
    open_set = set()
    closed_set = set()

    open_set.add(start_node)
    start_node.g_cost = 0
    start_node.f_cost = heuristic_func(start_node, goal_node)

    def find_lowest_f_cost_node(open_set):
        lowest_f_cost = float('inf')
        lowest_f_cost_node = None
        for node in open_set:
            if node.f_cost < lowest_f_cost:
                lowest_f_cost = node.f_cost
                lowest_f_cost_node = node
        return lowest_f_cost_node

    def reconstruct_path(goal_node):
        path = []
        current_node = goal_node

        while current_node.parent is not None:
            path.insert(0, current_node)
            current_node = current_node.parent

        path.insert(0, current_node)
        return path

    while len(open_set) > 0:
        current_node = find_lowest_f_cost_node(open_set)
        if current_node == goal_node:
            path = reconstruct_path(goal_node)
            return path

        open_set.remove(current_node)
        closed_set.add(current_node)

        for neighbor in get_neighbors(graph, current_node):
            if neighbor in closed_set:
                continue

            tentative_g_cost = current_node.g_cost + distance(current_node, neighbor)

            if neighbor not in open_set:
                open_set.add(neighbor)

            if tentative_g_cost < neighbor.g_cost:
                neighbor.g_cost = tentative_g_cost
                neighbor.h_cost = heuristic_func(neighbor, goal_node)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                neighbor.parent = current_node

    if not open_set:
        return []





