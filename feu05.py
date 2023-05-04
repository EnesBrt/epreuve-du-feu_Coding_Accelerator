import copy
import sys


# Lire le fichier labyrinthe.map
def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    labyrinthe = [list(line.strip()) for line in lines[1:]]
    return labyrinthe


# Afficher le résultat
def display_result(labyrinthe_with_path):
    for row in labyrinthe_with_path:
        print("".join(row))


# Trouver la l'entré et la sortie du labyrinthe
def find_start_and_exit(labyrinthe):
    for row in range(len(labyrinthe)):
        for col in range(len(labyrinthe[0])):
            if labyrinthe[row][col] == '1':
                entry = (row, col)
            elif labyrinthe[row][col] == '2':
                output = (row, col)
    return entry, output


# fonction qui convertit un labyrinthe en un graphe, en connectant les cases vides (y compris l'entrée et la sortie)
# à leurs voisins adjacents (haut, bas, gauche, droite) qui ne sont pas des murs
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


# Cette fonction calcule la distance entre deux points (nœuds) dans un tableau, en additionnant la
# différence absolue de leurs coordonnées x et y, cela donne une estimation simple de la distance à parcourir entre
# les deux points, sans prendre en compte les obstacles
def manhattan_distance(current_node, goal_node):
    current_node_x = current_node[0]
    current_node_y = current_node[1]

    goal_node_x = goal_node[0]
    goal_node_y = goal_node[1]

    diff_x = abs(current_node_x - goal_node_x)
    diff_y = abs(current_node_y - goal_node_y)

    manhattan_distance = diff_x + diff_y

    return manhattan_distance


# Fonction de l'algorithme A Star, c'est une fonction heuristique qui permet de trouver le chemin le plus court
def a_star_algorithm(graph, start_node, goal_node, heuristic_func):
    open_set = {start_node}
    closed_set = set()

    g_costs = {node: float('inf') for node in graph}
    g_costs[start_node] = 0

    f_costs = {node: float('inf') for node in graph}
    f_costs[start_node] = heuristic_func(start_node, goal_node)

    parents = {node: None for node in graph}

    # Cette fonction cherche le nœud ayant le coût le plus bas parmi les nœuds ouverts et le renvoie pour décider de
    # la prochaine étape à suivre dans la recherche du chemin
    def find_lowest_f_cost_node(open_set):
        lowest_f_cost = float('inf')
        lowest_f_cost_node = None
        for node in open_set:
            if f_costs[node] < lowest_f_cost:
                lowest_f_cost = f_costs[node]
                lowest_f_cost_node = node
        return lowest_f_cost_node

    # Cette fonction retrace le chemin le plus court entre deux points dans un labyrinthe en suivant les liens entre
    # les cases depuis la sortie jusqu'à l'entrée
    def reconstruct_path(parents, goal_node):
        path = []
        current_node = goal_node

        while current_node is not None:
            path.insert(0, current_node)
            current_node = parents[current_node]
        return path

    # Tant qu'il reste des nœuds à explorer, on choisit le nœud ayant le plus petit coût total (distance déjà
    # parcourue + distance estimée). Si ce nœud est la sortie, on reconstruit le chemin et on le renvoie. Sinon,
    # on marque ce nœud comme exploré et on continue
    while len(open_set) > 0:
        current_node = find_lowest_f_cost_node(open_set)
        if current_node == goal_node:
            path = reconstruct_path(parents, goal_node)
            return path

        open_set.remove(current_node)
        closed_set.add(current_node)

        # Cette partie du code examine les voisins du nœud actuel dans le labyrinthe, ignore ceux déjà explorés et
        # met à jour les coûts pour atteindre les voisins non explorés, en tenant compte de l'heuristique pour
        # trouver le chemin le plus court
        for neighbor in graph[current_node]:
            if neighbor in closed_set:
                continue

            tentative_g_cost = g_costs[current_node] + 1

            if neighbor not in open_set:
                open_set.add(neighbor)

            if tentative_g_cost < g_costs[neighbor]:
                g_costs[neighbor] = tentative_g_cost
                parents[neighbor] = current_node
                f_costs[neighbor] = g_costs[neighbor] + heuristic_func(neighbor, goal_node)

    # Si aucune case à explorer n'est trouvée, retournez un chemin vide, car il n'y a pas de solution pour atteindre
    # la sortie.
    if not open_set:
        return []


# trace le chemin le plus court trouvé
def trace_path_in_labyrinthe(labyrinthe, path):
    labyrinthe_copy = copy.deepcopy(labyrinthe)
    for i in range(1, len(path) - 1):
        row, col = path[i]
        labyrinthe_copy[row][col] = 'o'
    return labyrinthe_copy


# affiche le nombre de coups pour trouver la sortie
def number_attempts(labyrinthe_with_path):
    count_o = 0
    for row in range(len(labyrinthe_with_path)):
        for col in range(len(labyrinthe_with_path[0])):
            if labyrinthe_with_path[row][col] == 'o':
                count_o += 1
    print(f'SORTIE ATTEINTE EN {count_o} COUPS !')


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Usage: python script.py <labyrinthe_filename>")
        sys.exit()

    labyrinthe = read_file(filename)
    start, exit = find_start_and_exit(labyrinthe)
    graph = create_graph_from_labyrinthe(labyrinthe)
    shortest_path = a_star_algorithm(graph, start, exit, manhattan_distance)
    labyrinthe_with_path = trace_path_in_labyrinthe(labyrinthe, shortest_path)
    display_result(labyrinthe_with_path)
    number_attempts(labyrinthe_with_path)
