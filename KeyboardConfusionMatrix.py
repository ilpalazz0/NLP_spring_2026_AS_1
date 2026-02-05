import math
import unicodedata

def norm(text):
    return unicodedata.normalize('NFC', text)

keyboard_az = {
  
    'q': (0, 0), 'ü': (1, 0), 'e': (2, 0), 'r': (3, 0),
    't': (4, 0), 'y': (5, 0), 'u': (6, 0), 'i': (7, 0),
    'o': (8, 0), 'p': (9, 0), 'ö': (10, 0), 'ğ': (11, 0),
    '-': (12, 0),

    
    'a': (0.5, 1), 's': (1.5, 1), 'd': (2.5, 1), 'f': (3.5, 1),
    'g': (4.5, 1), 'h': (5.5, 1), 'j': (6.5, 1), 'k': (7.5, 1),
    'l': (8.5, 1), 'ı': (9.5, 1), 'ə': (10.5, 1),
    "'": (11.5, 1),
      

    
    'z': (1, 2), 'x': (2, 2), 'c': (3, 2), 'v': (4, 2),
    'b': (5, 2), 'n': (6, 2), 'm': (7, 2), 'ç': (8, 2),
    'ş': (9, 2)
}


#keyboard_az = {norm(k): v for k, v in keyboard_az.items()}

def distance(c1, c2, layout):
    x_1, y_1 = layout[c1]
    x_2, y_2 = layout[c2]
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

matrix_dist = {}

for c in keyboard_az:
    row = {}
    for k in keyboard_az:
        if c == k:
            row[k] = 1.0
        else:
            dist = distance(c, k, keyboard_az)
            row[k] = 1/(dist + 1)
    matrix_dist[c] = row

matrix_prob = {}

for c, row in matrix_dist.items():
    total = sum(row.values())
    matrix_prob[c] = {k: v/total for k, v in row.items()}

matrix_prob['i']['ı'] = max(matrix_prob['i']['ı'],0.7)
matrix_prob['ı']['i'] = max(matrix_prob['ı']['i'],0.7)
matrix_prob['ü']['u'] = max(matrix_prob['ü']['u'],0.7)
matrix_prob['u']['ü'] = max(matrix_prob['u']['ü'],0.7)
matrix_prob['ö']['o'] = max(matrix_prob['ö']['o'],0.7)
matrix_prob['o']['ö'] = max(matrix_prob['o']['ö'],0.7)
matrix_prob['ğ']['g'] = max(matrix_prob['ğ']['g'],0.7)
matrix_prob['g']['ğ'] = max(matrix_prob['g']['ğ'],0.7)
matrix_prob['e']['ə'] = max(matrix_prob['e']['ə'],0.7)
matrix_prob['ə']['e'] = max(matrix_prob['ə']['e'],0.7)
matrix_prob['ç']['c'] = max(matrix_prob['ç']['c'],0.7)
matrix_prob['c']['ç'] = max(matrix_prob['c']['ç'],0.7)
matrix_prob['ş']['s'] = max(matrix_prob['ş']['s'],0.7)
matrix_prob['s']['ş'] = max(matrix_prob['s']['ş'],0.7)


for c, row in matrix_prob.items():
    total = sum(row.values())
    for k in row:
        row[k] = row[k] / total

matrix_cost = {}

for c, row in matrix_prob.items():
    matrix_cost[c] = {k: -math.log(v) for k, v in row.items()}

