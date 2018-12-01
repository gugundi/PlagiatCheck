import articleReader
import os
from lsh import LSH
import time
import sys

filepath = sys.argv[1] # length of shingle

fast_lsh = LSH(mode="fast",threshold=0.001)
last_time = False
j = 0
while not last_time:
    articleDict, titleDict, last_time = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens", j)
    fast_lsh.buildSignatures(articleDict)
    #fast_lsh.buildSignaturesParallel(articleDict)
    j += 1

# LSH
f = open(filepath, 'r')
start = time.time()
print("====================================== LSH similarity ========================================")
sims = fast_lsh.findSimilarDocuments(f.read())
for sim in sims: print("| Sim: {:05.3f} | Cand: {:30d} |".format(sim[0],sim[1]))
print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))

