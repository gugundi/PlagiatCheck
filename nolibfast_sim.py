import sys
import os
import mmh3
import itertools
import time
import pickle
import struct

import numpy as np

from tqdm import tqdm


#################### Utilities ######################
#hashes a list of strings
def listhash(l,seed):
	val = 0
	for e in l:
		val = val ^ mmh3.hash(e, seed,signed=False)
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

def fastSignatures(docsDict:dict):
    # http://en.wikipedia.org/wiki/Mersenne_prime
    _mersenne_prime = (1 << 61) - 1
    _max_hash = (1 << 32) - 1
    _hash_range = (1 << 32)
    sigDict = {}

    generator = np.random.RandomState(1)
    a,b = np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64),
                                generator.randint(0, _mersenne_prime, dtype=np.uint64))
                                for _ in range(k)], dtype=np.uint64).T

    for key in tqdm(docsDict.keys()):
        #tokens = libShingle(q,docsDict[key])
        tokens = shingle(q,docsDict[key])
        hashvalues = np.ones(k, dtype=np.uint64)*_max_hash

        for to in tokens:
            #hv = struct.unpack('<I', sha1(to.encode('utf-8')).digest()[:4])[0]
            hv = listhash(to,1)
            phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash))
            hashvalues = np.minimum(phv, hashvalues)
        
        sigDict[key] = list(hashvalues)
    
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


def lsh_similar(sig_dic, docs, q, k, b, min_simi):
    r = int(k/b)
    bandDicts = []

    # Dictionary for each band
    # band_key = (r=k/b minhash values)
    # BandDict {band_key:[doc_keys1,doc_key2,...]}
    for ii in range(b):
        bandDict = {}

        # Every signature for every band
        for doc_key,value in sig_dic.items():
            band_key = tuple(value[ii*r:(ii+1)*r])
            #band_key = tuple(cut)
            if band_key not in bandDict.keys():
                bandDict[band_key] = [doc_key]
            else:
                bandDict[band_key].append(doc_key)
        
        bandDicts.append(bandDict)

 
    # Find candidates for each document
    sims = []
    for document in list(docs.keys()):
        candidates = []
        signature = sig_dic[document]

        for ii in range(b):
            band_key = tuple(signature[ii*r:(ii+1)*r])
            #band_key = tuple(cut)
            if band_key not in bandDicts[ii].keys():
                continue
            else:
                candidates.extend(bandDicts[ii][band_key])
        
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
k = 600 # number of minhashes
max_docs = 20
docs = {} #dictionary mapping document id to document contents
min_sim = 0.2
b = 40

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "ats_corpus")   # change to ats_corpus for large data set

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

#################### Testing #######################

def test(rebuildSigDict = False, debug = False, usePickle=False):
    
    # Rebuild flag can be set to force rebuilding the signatures
    if rebuildSigDict:
        #sigDict = signatures(docs)
        sigDict = fastSignatures(docs)
        if usePickle: pickle.dump( sigDict, open( "sigDict.p", "wb" ) )
    else:
        # If rebuild is False, then try and load the model,
        # if it doesnt exist, build it
        try:
            print("Loading signatures")
            start = time.time()
            sigDict = pickle.load(open("sigDict.p", "rb"))
            print("Loading signatures took: {}s".format(time.time() - start))
        except (OSError, IOError) as e:
            print("Going intro build mode")
            sigDict = signatures(docs)
            pickle.dump(sigDict, open("sigDict.p", "wb"))

    # All debug code should be placed in here
    if debug:
        shingles = [shingle(q,docs[doc]) for doc in docs]
        print("These are the first 5 shingles in first doc:")
        print(shingles[0][:5])

        print("These are the minhashes of these shingles:")
        print(minhash(shingles[0][:5],1))

        print("This is a part of the first signature in the signature dictionary")
        print("There are:", len(list(sigDict.values())), " signatures (one for each document)")
        print("Each signature consists of:", len(list(sigDict.values())[0]), " minhash values")
        print("Some of these values are: ", list(sigDict.values())[0][:5])


    # Jacard Sim
    start = time.time()
    print("===================================== Jacard similarity ======================================")
    sims = similar(sigDict, docs, k, min_sim)
    for sim in sims: print("|| Sim: {:05.3f} | Doc1: {:30s} | Doc2: {:30s} ||".format(sim[0],sim[1],sim[2]))
    print("========================================== Stats =============================================")
    print("||        Sims over threshold: {:2.0f}            |                   Time: {:2.3f}                ||".format(len(sims),time.time() - start))
    print("==============================================================================================")
    print("")

    # LSH
    start = time.time()
    print("====================================== LSH similarity ========================================")
    lsh_sims = lsh_similar(sigDict,docs,q,k,b,min_sim)
    for sim in lsh_sims: print("|| Sim: {:05.3f} | Doc: {:31s} | Cand: {:30s} ||".format(sim[0],sim[1],sim[2]))
    print("========================================== Stats =============================================")
    print("||        Sims over threshold: {:2.0f}            |                   Time: {:2.3f}                ||".format(len(lsh_sims),time.time() - start))
    print("==============================================================================================")

test(rebuildSigDict=True,debug=False,usePickle=False)
