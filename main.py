import os
import test_main
import sys


q = int(sys.argv[1]) # length of shingle
k = int(sys.argv[2]) # number of minhashes
b = int(sys.argv[3])
min_sim = float(sys.argv[4])
testMode = sys.argv[5].lower() == 'true'
docs = {} #dictionary mapping document id to document contents
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

if testMode:
    test_main.test(k, min_sim, docs, q, b, rebuildSigDict=False, debug=True)
else:
    print("LOL")

