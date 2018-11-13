import sys
import os
import mmh3
import itertools
import time
import pickle

from tqdm import tqdm


#################### Utilities ######################
#hashes a list of strings
def listhash(l,seed):
	val = 0
	for e in l:
		val = val ^ mmh3.hash(e, seed)
	return val 


def shingle(q,s):
    tokens = s.split(" ")
    return [tokens[i:i+q] for i in range(0,len(tokens) - q + 1)]    


def minhash(shin,k):
    return  [min([listhash(shi,seed) for shi in shin]) for seed in range(k)]


def signatures(docsDict:dict):
    sigDict = {}

    print("Creating signatures")
    for key in tqdm(docsDict.keys()):
        shin = shingle(q,docsDict[key])
        minh = minhash(shin,k)
        sigDict[key] = minh
    return sigDict


def jacard(sig_dic,doc1,doc2):
    a = set(sig_dic[doc1])
    b = set(sig_dic[doc2])

    return float(len(a & b)) / len(a | b)


def estJacard(sig_dic,doc1,doc2,k):
    a = set(sig_dic[doc1])
    b = set(sig_dic[doc2])

    return len(a & b)/k


def similar(sig_dic, docs, k, min_simi):
    sims = []

    for pair in itertools.combinations(docs.keys(), 2):
        sim = estJacard(sig_dic,pair[0],pair[1],k)
        if sim > min_simi:
            sims.append([sim,pair[0],pair[1]])

    sims.sort(key=lambda x: float(x[0]))
    return sims

#New implementation of Locality Sensitive Hashing
def LSH(sig_Dict):
    #Build dictionary for each band
    for i in range(b):
        bandDict = {}
        for key, value in sig_Dict.items():
            #Tuple is used because lists can not be used as keys
            bandKey = tuple(value[int(rows*i):int(rows*(i+1))])
            bandValue = key
            if bandKey not in bandDict:
                bandDict[bandKey] = [bandValue]
            else:
                bandDict[bandKey].append(bandValue)
        bandDicts[i] = bandDict
    return bandDicts

#Compute candidates to a signature
def computeCandidates(sig):
    cand = set()
    for i in range(b):
        sigKey = tuple(sig[int(rows*i):int(rows*(i+1))])
        if sigKey in bandDicts[i]:
            cand.update(bandDicts[i][sigKey])
    return cand

#Computes the similarity of a document to the candidates
def compCandSimilarity(sic_dic, doc, cands, sim):
    measures = []
    for cand in cands:
        if not (cand == doc):
            simi = estJacard(sic_dic,doc,cand,k)
            if (simi >= sim):
                measures.append([simi,doc,cand])
    return measures

def lsh_similar(sig_dic, docs, q, k, b, min_simi):
    r = int(k/b)
    bandDicts = []

    # Dictionary for each band
    for ii in range(b):
        bandDict = {}

        # Every signature for every band
        for key,value in sig_dic.items():
            cut = value[ii*r:(ii+1)*r]
            bandkey = tuple(cut)
            if bandkey not in bandDict.keys():
                bandDict[bandkey] = [key]
            else:
                bandDict[bandkey].append(key)
        
        bandDicts.append(bandDict)

 
    # Find candidates for each document
    sims = []
    for document in list(docs.keys()):
        candidates = []
        signature = sig_dic[document]

        for ii in range(b):
            cut = signature[ii*r:(ii+1)*r]
            bandkey = tuple(cut)
            if bandkey not in bandDicts[ii].keys():
                continue
            else:
                candidates.extend(bandDicts[ii][bandkey])
        
        # For each candidate, see if they have a high similarity
        candidates = set(candidates)
        for candidate in candidates:
            if candidate == document:
                continue

            sim = estJacard(sig_dic, document, candidate,k)
            if sim > min_simi:
                if [sim,candidate,document] not in sims:
                    sims.append([sim,document,candidate])
    sims.sort(key=lambda x: float(x[0]))
    return sims

################### Similarity ######################
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

#################### Testing #######################

def test(rebuildSigDict = False, debug = False):
    # Rebuild flag can be set to force rebuilding the signatures
    if rebuildSigDict:
        sigDict = signatures(docs)
        pickle.dump( sigDict, open( "sigDict.p", "wb" ) )
    else:
        # If rebuild is False, then try and load the model,
        # if it doesnt exist, build it
        try:
            sigDict = pickle.load(open("sigDict.p", "rb"))
        except (OSError, IOError) as e:
            sigDict = signatures(docs)
            pickle.dump(sigDict, open("sigDict.p", "wb"))

    # All debug code should be placed in here
    if debug:
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
    start = time.time()
    print("===================================== Jacard similarity ======================================")
    sims = similar(sigDict, docs, k, min_sim)
    for sim in sims: print("| Sim: {:05.3f}   | Doc1: {:30s} | Doc2: {:30s} |".format(sim[0],sim[1],sim[2]))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))
    print("")
    
    # LSH
    start = time.time()
    print("====================================== LSH similarity ========================================")
    lsh_sims = lsh_similar(sigDict,docs,q,k,b,min_sim)
    for sim in lsh_sims: print("| Sim: {:05.3f}   | Doc: {:31s} | Cand: {:30s} |".format(sim[0],sim[1],sim[2]))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))

test(rebuildSigDict=False)