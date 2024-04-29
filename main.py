import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__(self, n, t1_range, t2_range, t3_range):
        self.n = n
        self.t1_range = t1_range
        self.t2_range = t2_range
        self.t3_range = t3_range
        self.matrix = np.full((n, n), float('inf'))
        self.build_network()
        self.distances, self.routing_table = self.floyd_warshall()

    def dfs_recursive(self, node, visited, cpt):
        visited[node] = True
        cpt += 1
        for i in range(self.n):
            if self.matrix[node][i] != float('inf') and not visited[i]:
                cpt = self.dfs_recursive(i, visited, cpt)
        return cpt

    def is_connex(self):
        node = 0
        visited = [False] * self.n
        cpt = 0
        return self.dfs_recursive(node, visited, cpt) == self.n

    def count_links(self, line, starting_column=0):
        cpt = 0
        for i in range(starting_column, self.n):
            if self.matrix[line][i] != float('inf'):
                cpt += 1
        return cpt

    def change_tier1(self, x):
        for y in range(x + 1, self.t1_range):
            if random.random() < 0.75:
                link_value = random.randint(5, 10)
                self.matrix[y][x] = link_value
                self.matrix[x][y] = link_value

    def change_tier2_to_backbone(self, x):
        backbone_nodes = random.sample(range(self.t1_range), random.randint(1, 2))
        for y in backbone_nodes:
            rd_nb = random.randint(10, 20)
            self.matrix[x][y] = rd_nb
            self.matrix[y][x] = rd_nb

    def change_tier2(self):
        degree_list = [[i, 0] for i in range(self.t1_range, self.t2_range)]
        random.shuffle(degree_list)
        while True:
            if degree_list[0][1] >= 2:
                break
            else:
                for i in range(1, len(degree_list)):
                    if self.matrix[degree_list[i][0]][degree_list[0][0]] == float('inf'):
                        # Updating matrix
                        rd_nbr = random.randint(10, 20)
                        self.matrix[degree_list[i][0]][degree_list[0][0]] = rd_nbr
                        self.matrix[degree_list[0][0]][degree_list[i][0]] = rd_nbr
                        # Updating degrees
                        degree_list[0][1] += 1
                        degree_list[i][1] += 1
                        break

            degree_list = sorted(degree_list, key=lambda x: x[1])

    def change_tier3(self):
        for x in range(self.t2_range, self.t3_range):
            t2_nodes = random.sample(range(self.t1_range, self.t2_range), 2)
            for y in t2_nodes:
                rd_nbr = random.randint(20, 50)
                self.matrix[x][y] = rd_nbr
                self.matrix[y][x] = rd_nbr

    def build_network(self):
        for x in range(self.t1_range):
            self.change_tier1(x)
        for x in range(self.t1_range, self.t2_range):
            self.change_tier2_to_backbone(x)
        self.change_tier2()
        self.change_tier3()

    def get_distances(self):
        distance = list(self.matrix.copy())
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        return distance

    def floyd_warshall(self):

        dist = [[self.matrix[i][j] for j in range(self.n)] for i in range(self.n)]
        routing_table = [[j if self.matrix[i][j] != float('inf') else -1 for j in range(self.n)] for i in range(self.n)]
        for i in range(self.n):
            dist[i][i] = 0
            routing_table[i][i] = i

        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        routing_table[i][j] = routing_table[i][k]

        return dist, routing_table

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
