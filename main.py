import random
import numpy as np


def create_backbone(nodes_numbers: int) -> np.array:
    tab = np.full((nodes_numbers, nodes_numbers), -1)
    for i in range(nodes_numbers):
        for j in range(i + 1, nodes_numbers):
            if random.random() < 0.75:
                a = random.randint(5, 10)
                tab[i][j] = a
                tab[j][i] = a

    return tab
 

print(create_backbone(5))

