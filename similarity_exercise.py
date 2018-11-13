import sys
import os
import mmh3
import itertools


#################### Utilities ######################
#hashes a list of strings
def listhash(l,seed):
	val = 0
	for e in l:
		val = val ^ mmh3.hash(e, seed)
	return val 



################### Similarity ######################
q = 3 # length of shingle
k = 100 # number of minhashes
docs = {} #dictionary mapping document id to document contents

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "ats_corpus_small")   # change to ats_corpus for large data set

for file in os.listdir(datafolder):
    filepath = os.path.join(datafolder, file)
    f = open(filepath, 'r')
    docs[file] = f.read()
    print("read document " + file)
    f.close()

def shingle(q,s:str):
    tokens = s.split()
    shingles = [tokens[i:i+q] for i in range(len(tokens) - q + 1) if len(tokens[i]) < 4]
    return shingles

def minhash(shin,k):
    return  [min([listhash(shi,seed) for shi in shin]) for seed in range(k)]

def signatures(docsDict:dict):
    sigDict = {}

    for key in docsDict.keys():
        print(key)
        shin = shingle(q,docsDict[key])
        minh = minhash(shin,k)
        sigDict[key] = minh
    return sigDict

sigDict = signatures(docs)

def jacard(doc1,doc2):
    a = set(sigDict[doc1])
    b = set(sigDict[doc2])
    c = a.intersection(b)
    #print("Estimated Jacard: ", len(c)/k)
    #print("Exact Jacard: ", float(len(c)) / (len(a) + len(b) - len(c)))

    return len(c)/k
    #return float(len(c)) / (len(a) + len(b) - len(c))

def similar():
    for pair in itertools.combinations(docs.keys(), 2):
        print("{0} - similarity for {1} and {2}".format(jacard(pair[0],pair[1]),pair[0],pair[1]))

def test():
    shingles = [shingle(q,docs[doc]) for doc in docs]
    print("These are the first 5 shingles in first doc:")
    print(shingles[0][:5])

    print("These are the minhashes of these shingles:")
    print(minhash(shingles[0][:4],2))

    print("This is a part of the first signature in the signature dictionary")
    print("There are:", len(list(sigDict.values())), " signatures (one for each document)")
    print("Each signature have:", len(list(sigDict.values())[0]), " different hashes")
    print("Some of these values are: ", list(sigDict.values())[0][:5])

    # Jacard Sim
    similar()

test()