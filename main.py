import re
import math
import matplotlib.pyplot as plt
import numpy as np
import LevensteinBK 
import unicodedata
from nltk.probability import FreqDist


def norm(text):
    return unicodedata.normalize('NFC', text)

with open("Fuzuli-I.txt", "r", encoding="utf-8") as infile:
    content = infile.read()

content = content.lower()
cleaned = "".join(char if char.isalpha() else " " for char in content)
tokens = re.findall(r"\b[^\W\d_]+(?:[\'’\-][^\W\d_]+)*\b", content)
tokens = [t.replace("’", "'") for t in tokens]
freqDist = FreqDist(tokens)
vocab = set()

for token in tokens:
    vocab.add(token)

tt = LevensteinBK.BKtree(vocab)
search_word = "ölmaz"
res = tt.search(search_word, 2)
sorted_res = sorted(res, key = lambda w:( LevensteinBK.WeightedLevenstein(w.label, search_word)))

for i in sorted_res:
    print(i)
