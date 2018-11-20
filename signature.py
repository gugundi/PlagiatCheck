from tqdm import tqdm
from shingle import shingle
from minHash import minhash, listhash
import numpy as np

def signatures(docsDict:dict,q, k):
    sigDict = {}

    print("Creating signatures")
    for key in tqdm(docsDict.keys()):
        shin = shingle(q,docsDict[key])
        minh = minhash(shin,k)
        sigDict[key] = minh
    return sigDict

def docSignature(doc, q, k):
    return minhash(shingle(q,doc),k)

def fastSignatures(docsDict:dict, q, k, seed):
    # Inspiration from https://github.com/ekzhu/datasketch/blob/master/datasketch/minhash.py
    # http://en.wikipedia.org/wiki/Mersenne_prime
    _mersenne_prime = (1 << 61) - 1
    _max_hash = (1 << 32) - 1
    _hash_range = (1 << 32)
    sigDict = {}

    generator = np.random.RandomState(seed)
    a,b = np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64),
                                generator.randint(0, _mersenne_prime, dtype=np.uint64))
                                for _ in range(k)], dtype=np.uint64).T

    for key in tqdm(docsDict.keys()):

        shingles = shingle(q,docsDict[key])
        hashvalues = np.ones(k, dtype=np.uint64)*_max_hash

        for shin in shingles:
            hv = listhash(shin,seed)
            # https://en.wikipedia.org/wiki/Universal_hashing
            phv = np.bitwise_and((a * hv + b) % _mersenne_prime, np.uint64(_max_hash))
            hashvalues = np.minimum(phv, hashvalues)
        
        sigDict[key] = list(hashvalues)
    
    return sigDict