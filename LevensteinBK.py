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
            distance = Levenstein(label, current.label)

            while distance in current.children.keys():
                current = current.children.get(distance)
                distance = Levenstein(label, current.label)
            current.children[distance] = node
    
    def search(self, label, max_dist):
        candidates = deque([self.root])
        found = []

        while len(candidates) > 0:
            node = candidates.popleft()
            distance = Levenstein(label, node.label)

            if(distance <= max_dist):
                found.append(node)

            candidates.extend(child_node for child_dist, child_node in node.children.items()
                              if distance - max_dist <= child_dist <= distance + max_dist)
        
        return found


def Levenstein(a, b):
    n = len(a)
    m = len(b)

    lev = np.zeros((n+1, m+1))

    for i in range (0, n+1):
        lev[i, 0] = i

    for i in range (0, m+1):
        lev[0, i] = i

    for i in range (1, n+1):
        for j in range (1, m+1):
            insertion = lev[i - 1, j] + 1
            deletion = lev[i, j - 1] + 1
            substitution = lev[i-1, j-1] + (1 if (a[i-1] != b[j-1])  else 0)
            lev[i, j] = min(insertion, deletion, substitution)
    
    return lev[n, m]
