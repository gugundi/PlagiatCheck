import articleReader
import os
from lsh import LSH
import time

articleDict, titleDict = articleReader.findArticles("PlagiatCheck/Dataset/wikitext-2/wiki.train.tokens")

docs = {} #dictionary mapping document id to document contents
max_docs = 700

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "Dataset/ats_corpus")   # change to ats_corpus for large data set

i = 0
for file in os.listdir(datafolder):
    filepath = os.path.join(datafolder, file)
    f = open(filepath, 'r')
    if str(file).startswith("."):
        continue

    docs[file] = f.read()
    #print("read document " + file)
    f.close() 
    i+= 1
    if i == max_docs: break

def test(docDict=docs):
    fast_lsh = LSH(mode="fast",threshold=0.2)
    #fast_lsh.buildSignatures(docDict)
    fast_lsh.buildSignaturesParallel(docDict)

    # LSH
    start = time.time()
    print("====================================== LSH similarity ========================================")
    sims = fast_lsh.computeInternalSimilarities()
    for sim in sims: print("| Sim: {:05.3f}   | Doc: {:31d} | Cand: {:30d} |".format(sim[0],sim[1],sim[2]))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))

test(articleDict)
