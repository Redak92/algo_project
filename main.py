import random
import numpy as np


class Network:
    def __init__(self, n, t1_range, t2_range, t3_range):
        self.n = n
        self.t1_range = t1_range
        self.t2_range = t2_range
        self.t3_range = t3_range
        self.matrix = np.full((n, n), float('inf'))
        self.build_network()
        self.paths = self.routing_table()

    def dfs_recursive(self, node, visited, cpt):
        visited[node] = True
        cpt += 1
        for i in range(self.n):
            if self.matrix[node][i] != float('inf') and visited[i] == False:
                cpt = self.dfs_recursive(i, visited, cpt)
        return cpt

    def is_connexe(self):
        node = 0
        visited = [False] * self.n
        cpt = 0
        return self.dfs_recursive(node, visited, cpt)

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
            #fix it
    def change_tier_2(self):
        pass

    def build_network(self):
        for x in range(self.t1_range):
            self.change_tier1(x)
        for x in range(self.t1_range, self.t2_range):
            self.change_tier2_to_backbone(x)


    def routing_table(self):
        distance = list(map(lambda i: list(map(lambda j: j, i)), self.matrix.copy()))
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
        return distance


a = Network(10, 5, 10, 20)
a.build_network()
print(a.matrix)
for i in range(10):
    print(a.count_links(i))