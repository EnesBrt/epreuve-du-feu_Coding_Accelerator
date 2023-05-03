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

# Fonction pour créer un graphe à partir d'un labyrinthe en associant chaque case vide, l'entrée et la sortie aux
# noeuds et en connectant les noeuds adjacents qui ne sont pas des murs.
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


# Calcule la distance de Manhattan entre deux points (current_node et goal_node) en utilisant leurs coordonnées (x, y).
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
    # # Initialise les ensembles open_set et closed_set, les coûts g et f, et les parents pour tous les nœuds du
    # graphe, en définissant les coûts de départ et les parents du nœud de départ.
    open_set = {start_node}
    closed_set = set()

    g_costs = {node: float('inf') for node in graph}
    g_costs[start_node] = 0

    f_costs = {node: float('inf') for node in graph}
    f_costs[start_node] = heuristic_func(start_node, goal_node)

    parents = {node: None for node in graph}

    # Fonction pour trouver le nœud ayant le coût F le plus bas (coût total estimé) parmi les nœuds dans l'ensemble
    # ouvert (nœuds à explorer)
    def find_lowest_f_cost_node(open_set):
        lowest_f_cost = float('inf')
        lowest_f_cost_node = None
        for node in open_set:
            if f_costs[node] < lowest_f_cost:
                lowest_f_cost = f_costs[node]
                lowest_f_cost_node = node
        return lowest_f_cost_node

    # # fonction qui retrace le chemin le plus court trouvé par l'algorithme de recherche, en partant du nœud
    # d'arrivée et en remontant jusqu'au nœud de départ à l'aide du dictionnaire "parents".
    def reconstruct_path(parents, goal_node):
        path = []
        current_node = goal_node

        while current_node is not None:
            path.insert(0, current_node)
            current_node = parents[current_node]

        return path

    # Tant qu'il reste des nœuds à explorer, sélectionne le nœud avec le coût total le plus faible, vérifie si
    # c'est le nœud d'arrivée, construit le chemin si c'est le cas, sinon, continue à explorer les voisins.
    while len(open_set) > 0:
        current_node = find_lowest_f_cost_node(open_set)
        if current_node == goal_node:
            path = reconstruct_path(parents, goal_node)
            return path

        open_set.remove(current_node)
        closed_set.add(current_node)

            # Parcourt les voisins du nœud courant, ignore les voisins déjà explorés (dans closed_set),
            # met à jour les coûts et les parents des voisins non explorés,
            # et ajoute les voisins au prochain ensemble de nœuds à explorer (open_set).
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


    # Si l'ensemble des noeuds ouverts est vide,
    # cela signifie que nous avons exploré toutes les options possibles sans atteindre la sortie,
    # alors on retourne un chemin vide (aucun chemin trouvé).
    if not open_set:
        return []


# trace le chemin le plus court trouvé
def trace_path_in_labyrinthe(labyrinthe, path):
    labyrinthe_copy = copy.deepcopy(labyrinthe)
    for i in range(1, len(path) - 1):  # Commencez à 1 pour éviter l'entrée, et arrêtez-vous avant la sortie
        row, col = path[i]  # Récupérez les coordonnées de la case du chemin
        labyrinthe_copy[row][col] = 'o'  # Modifiez la case correspondante dans la copie du labyrinthe avec 'o'

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
