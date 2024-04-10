import random

def create_backbone():
    dictio = {'T1-' + str(i + 1): {} for i in range(10)}
    for key, value in dictio.items():
        for node in dictio.keys():
            if node != key and random.random() >= 7.5:
                