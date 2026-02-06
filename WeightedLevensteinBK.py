import KeyboardConfusionMatrix
import numpy as np
from collections import deque

class Node:
    def __init__(self, label):
        self.label = label
        self.children = {}
    
    def __str__(self):
        return self.label
    
class BKtree:
    def __init__(self, labels = None):
        self.root = None
        if labels:
            for i in labels:
                self.add(i)

    def add(self, label):
        if self.root is None:
            self.root = Node(label)
        else:
            node = Node(label)
            current = self.root
            distance = WeightedLevenstein(label, current.label)

            while distance in current.children.keys():
                current = current.children.get(distance)
                distance = WeightedLevenstein(label, current.label)
            current.children[distance] = node
    
    def search(self, label, max_dist):
        candidates = deque([self.root])
        found = []

        while len(candidates) > 0:
            node = candidates.popleft()
            distance = WeightedLevenstein(label, node.label)

            if(distance <= max_dist):
                found.append(node)

            candidates.extend(child_node for child_dist, child_node in node.children.items()
                              if distance - max_dist <= child_dist <= distance + max_dist)
        
        return found


def WeightedLevenstein(a, b):
    n, m = len(a), len(b)
    lev = np.zeros((n+1, m+1))
    vowels = "üöıəeuoa"

    for i in range(1, n+1):
        lev[i, 0] = lev[i-1, 0] + (1 if a[i-1] in vowels else 0.5)

    for j in range(1, m+1):
        lev[0, j] = lev[0, j-1] + (1 if b[j-1] in vowels else 0.5)

    for i in range(1, n+1):
        for j in range(1, m+1):
            ins = lev[i-1, j] + (1 if a[i-1] in vowels else 0.5)
            dele = lev[i, j-1] + (1 if b[j-1] in vowels else 0.5)

            if a[i-1] == b[j-1]:
                sub_cost = 0
            elif (a[i-1] in KeyboardConfusionMatrix.matrix_cost and
                  b[j-1] in KeyboardConfusionMatrix.matrix_cost[a[i-1]]):
                sub_cost = KeyboardConfusionMatrix.matrix_cost[a[i-1]][b[j-1]]
            else:
                sub_cost = 1.0

            sub = lev[i-1, j-1] + sub_cost
            lev[i, j] = min(ins, dele, sub)

    return lev[n, m]
