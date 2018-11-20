import os
import test_main


q = 3 # length of shingle
k = 100 # number of minhashes
docs = {} #dictionary mapping document id to document contents
min_sim = 0.15
b = 20
rows = int(k/b)
bandDicts = {}

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "../DataandTemplate/ats_corpus_small")   # change to ats_corpus for large data set

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
    if i == 100: break

test_main.test(k, min_sim, docs, q, b, rebuildSigDict=False, debug=True)