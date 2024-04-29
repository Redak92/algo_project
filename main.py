import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# la classe Network permet de créer un réseau de n noeuds
# elle prend en paramètre n, t1_range, t2_range, t3_range
# n est le nombre de noeuds
# t1_range est le noeud de fin (non inclus) du tier 1
# t2_range est le noeud de fin (non inclus) du tier 2
# t3_range est le noeud de fin (non inclus) du tier 3
class Network:
    def __init__(self, n, t1_range, t2_range, t3_range):
        self.n = n
        self.t1_range = t1_range
        self.t2_range = t2_range
        self.t3_range = t3_range
        self.matrix = np.full((n, n), float('inf'))
        self.build_network()
        self.distances, self.routing_table = self.floyd_warshall()

    # la fonction dfs_recursive permet de parcourir le graphe en profondeur
    def dfs_recursive(self, node, visited, cpt):
        visited[node] = True
        cpt += 1
        for i in range(self.n):
            if self.matrix[node][i] != float('inf') and not visited[i]:
                cpt = self.dfs_recursive(i, visited, cpt)
        return cpt

    # la fonction is_connex permet de vérifier si le graphe est connexe
    # grace à la fonction dfs_recursive (parcours en profondeur)
    # si le nombre de noeuds visités est égal au nombre de noeuds du graphe alors le graphe est connexe
    def is_connex(self):
        node = 0
        visited = [False] * self.n
        cpt = 0
        return self.dfs_recursive(node, visited, cpt) == self.n

    # la fonction count_links permet de compter le degré d'un sommet
    def count_links(self, line, starting_column=0):
        cpt = 0
        for i in range(starting_column, self.n):
            if self.matrix[line][i] != float('inf'):
                cpt += 1
        return cpt

    # la fonction change_tier1 permet de lier les noeuds du tier 1 entre eux
    # elle remplit la matrice avec les distances entre les nœuds correspondants
    def change_tier1(self, x):
        for y in range(x + 1, self.t1_range):
            if random.random() < 0.75:
                link_value = random.randint(5, 10)
                self.matrix[y][x] = link_value
                self.matrix[x][y] = link_value

    # fonction qui permet de lier les noeuds du tier 2 au backbone
    def change_tier2_to_backbone(self, x):
        backbone_nodes = random.sample(range(self.t1_range), random.randint(1, 2))
        for y in backbone_nodes:
            link_value = random.randint(10, 20)
            self.matrix[x][y] = link_value
            self.matrix[y][x] = link_value

    # la fonction change_tier2 permet de lier les noeuds du tier 2 entre eux
    # elle fait en sorte que les degrés des sommets soient considérés comme valide (soit 2 soit 3) 
    def change_tier2(self):
        # on initialise une matrice de tous les degrés des noeuds
        degree_list = [[i, 0] for i in range(self.t1_range, self.t2_range)]
        random.shuffle(degree_list)
        while True:
            # tant que le premier élement n'est pas de degré 2 ou plus
            if degree_list[0][1] >= 2:
                break
            else:
                for i in range(1, len(degree_list)):
                    if self.matrix[degree_list[i][0]][degree_list[0][0]] == float('inf'):
                        # on update la matrice
                        rd_nbr = random.randint(10, 20)
                        self.matrix[degree_list[i][0]][degree_list[0][0]] = rd_nbr
                        self.matrix[degree_list[0][0]][degree_list[i][0]] = rd_nbr
                        # et on update les degrés 
                        degree_list[0][1] += 1
                        degree_list[i][1] += 1
                        break
            
            # on trie la liste afin de voir si le degré minimal est au moins 2
            degree_list = sorted(degree_list, key=lambda x: x[1])

    # la fonction change_tier3 permet de lier les noeuds du tier 3 entre eux
    def change_tier3(self):
        for x in range(self.t2_range, self.t3_range):
            t2_nodes = random.sample(range(self.t1_range, self.t2_range), 2)
            for y in t2_nodes:
                link_value = random.randint(20, 50)
                self.matrix[x][y] = link_value
                self.matrix[y][x] = link_value

    # la fonction build_network utilise les fonctions implémentées au dessus afin de construire le réseau integralement
    def build_network(self):
        for x in range(self.t1_range):
            self.change_tier1(x)
        for x in range(self.t1_range, self.t2_range):
            self.change_tier2_to_backbone(x)
        self.change_tier2()
        self.change_tier3()

    # la fonction floyd_warshall permet de construire la table de routage grace à l'algorithme de floyd-warshall
    def floyd_warshall(self):
        # on crée une copie de la matrice
        dist = [[self.matrix[i][j] for j in range(self.n)] for i in range(self.n)]

        # on crée une table de routage en remplacant les float inf par -1
        routing_table = [[j if self.matrix[i][j] != float('inf') else -1 for j in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            # la diagonale contiendra des zéros car la distance entre un noeud et lui même est 0
            dist[i][i] = 0
            # dans la diagonale de la table de routage contiendra la valeur de sa colonne/ligne
            routing_table[i][i] = i

        # on utilise l'algorithme de floyd-warshall pour construire la table de routage
        # on cherche le plus court chemin de chaque noeud vers tous les noeuds 
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        routing_table[i][j] = routing_table[i][k]

        return dist, routing_table


    # la fonction get_full_path utilise la table de routage pour determiner le plus court chemin entre les noeuds start et end
    def get_full_path(self, start, end):
        if self.routing_table[start][end] == -1:
            return []
        path = [start]
        current = start

        while current != end:
            next_hop = self.routing_table[current][end]
            if next_hop == -1:
                return []
            path.append(next_hop)
            current = next_hop

        return path

    # cette fonction permet de visualiser le graphe grace à networkx et matplotlib
    def show_graph(self):
        g = nx.Graph()
        for i in range(self.n):
            for j in range(i + 1, self.n):
                weight = self.matrix[i][j]
                if weight != float('inf'):
                    g.add_edge(i, j, weight=weight)
        pos = nx.spring_layout(g)
        nx.draw(g, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
        plt.title('Graph from an adjacency matrix')
        plt.show()


if __name__ == '__main__':
    a = Network(10, 3, 6, 10)
    print(a.matrix)
    print(a.distances)
    print(a.get_full_path(0, 9))
    a.show_graph()
