import mmh3
import random
import numpy as np

# http://en.wikipedia.org/wiki/Mersenne_prime
_mersenne_prime = (1 << 61) - 1
_max_hash = (1 << 32) - 1
_hash_range = (1 << 32)

class MinHash(object):


    def __init__(self, k=200, seed=1, shin_len=3, mode=None):

        self.k = k
        self.seed = seed
        self.shinlen = shin_len
        self.mode = mode
        
        if k > _hash_range:
            raise ValueError("Cannot have more than %d number of\
                    permutation functions" % _hash_range)

        generator = np.random.RandomState(self.seed)

        # http://en.wikipedia.org/wiki/Universal_hashing
        self.a, self.b = np.array([(generator.randint(1, _mersenne_prime, dtype=np.uint64),
                                    generator.randint(0, _mersenne_prime, dtype=np.uint64))
                                    for _ in range(k)], dtype=np.uint64).T  
    
    def _init_hashvalues(self):
        return np.ones(self.k, dtype=np.uint64)*_max_hash

    def shingles(self,doc):
        tokens = doc.split(" ")
        return ["-".join(tokens[i:i+self.shinlen]) for i in range(len(tokens)-self.shinlen + 1)]

    def signature(self,doc):
        if self.mode == "fast":
            return self.computeFastMinHash(doc)
        elif self.mode == "medium":
            return self.computeMediumMinHash(doc)
        elif self.mode == "16bit":
            return self.compute16bitHash(doc)
        else:
            return self.computeMinHash(doc)

    def computeMinHash(self,doc):
        shingles = self.shingles(doc)
        return [min([mmh3.hash(shi,seed) for shi in shingles]) for seed in range(self.seed,self.k+self.seed)]

    def computeMediumMinHash(self,doc):
        shingles = self.shingles(doc)
        hv = min([mmh3.hash(shi,self.seed) for shi in shingles]) 
        return [mmh3.hash(str(hv),seed) for seed in range(self.seed+1,self.seed+self.k)]

    def _split128to16(self,s):
        _16bitmask = (1 << 16) - 1
        return [(s>>(i*16) & _16bitmask) for i in range(8)]

    def compute16bitHash(self,doc):
        shingles = self.shingles(doc)
        hashvalues = self._init_hashvalues()

        for shin in shingles:
            phvs = [mmh3.hash128(shin,i) for i in range(int(self.k/8))]
            finalphv = []
            for phv in phvs:
                for v in self._split128to16(phv):
                    finalphv.append(v)
            hashvalues = np.minimum(finalphv, hashvalues)

        return hashvalues
        

    def computeFastMinHash(self,doc):
        shingles = self.shingles(doc)
        hashvalues = self._init_hashvalues()
    
        for shin in shingles:
            hv = mmh3.hash(shin,self.seed,signed=False)
            # https://en.wikipedia.org/wiki/Universal_hashing
            phv = np.bitwise_and((self.a * hv + self.b) % _mersenne_prime, np.uint64(_max_hash))
            hashvalues = np.minimum(phv, hashvalues)
        
        return hashvalues
    