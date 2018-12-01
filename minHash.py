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
        self.c = np.array([generator.randint(0, _hash_range,dtype=np.uint32) for _ in range(k)],dtype=np.uint32).T

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
        else:
            return self.computeMinHash(doc)

    def computeMinHash(self,doc):
        shingles = self.shingles(doc)
        return [min([mmh3.hash(shi,seed) for shi in shingles]) for seed in range(self.seed,self.k+self.seed)]

    def computeMediumMinHash(self,doc):
        shingles = self.shingles(doc)
        hashvalues = self._init_hashvalues()

        for shin in shingles:
            hv = mmh3.hash(shin,self.seed,signed=False)
            # https://en.wikipedia.org/wiki/Universal_hashing
            phv = np.bitwise_and((self.a * hv + self.b) % _mersenne_prime, np.uint64(_max_hash))
            hashvalues = np.minimum(phv, hashvalues)

        return hashvalues

    def computeFastMinHash(self,doc):
        shingles = self.shingles(doc)
        hashvalues = self._init_hashvalues()

        for shin in shingles:
            hv = mmh3.hash(shin,self.seed,signed=False)
            # https://en.wikipedia.org/wiki/Universal_hashing
            phv = np.bitwise_xor(self.c,hv)
            hashvalues = np.minimum(phv, hashvalues)
        return hashvalues
