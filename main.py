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
#cleaned = re.sub(r"\s+", " ", cleaned).strip()

#with open("Fuzuli-I-clean.txt", "w", encoding="utf-8") as outfile:
    #outfile.write(cleaned)




#with open("Fuzuli-I-clean.txt", "r", encoding="utf-8") as infile:
   # content = infile.read()

#tokens = content.split()
tokens = re.findall(r"\b[^\W\d_]+(?:[\'’\-][^\W\d_]+)*\b", content)
tokens = [t.replace("’", "'") for t in tokens]
freqDist = FreqDist(tokens)

#for token, frequency in freqDist.items():
#    print(f"{token} : {frequency}")

#print(tokens)
#print(len(tokens))


#freqDist.plot(100)
#plt.show()

step = 1000
N = []
V = []

vocab = set()

for i, token in enumerate(tokens, start = 1):
    vocab.add(token)
    
    if i % step == 0:
        N.append(i)
        V.append(len(vocab))

#vocab = {norm(k) for k in vocab}

plt.plot(N, V)
plt.xlabel("Number of tokens")
plt.ylabel("Vocabulary size")
plt.title("Heap's Law")
#plt.show()

logN = [math.log(n) for n in N]
logV = [math.log(v) for v in V]

plt.plot(logN, logV)
plt.xlabel("log N")
plt.ylabel("log V")
plt.title("Heaps' Law (log-log)")
#plt.show()

beta, logk = np.polyfit(logN, logV, 1)
k = math.exp(logk)

#print("beta =", beta)
#print("k =", k)

plt.plot(N, V)
plt.plot(N, (k)*(N**(beta)))
#plt.show()

tt = LevensteinBK.BKtree(vocab)
search_word = "ölmaz"
res = tt.search(search_word, 2)
sorted_res = sorted(res, key = lambda w:( LevensteinBK.WeightedLevenstein(w.label, search_word)))

for i in sorted_res:
    print(i)


#print(vocab)
