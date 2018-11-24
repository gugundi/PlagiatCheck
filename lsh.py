import pickle
from tqdm import tqdm
from minHash import MinHash

class LSH(object):

    def __init__(self, mode = None, sigDict=None, k=200, shinlen=3, b=10, seed=1,threshold=0.4):
        self.k = k
        self.b = b
        self.mode = mode
        self.shinlen = shinlen
        self.threshold = threshold

        # Check if k%b == 0
        self.rows = int(self.k/self.b)
        self.minHash = MinHash(self.k, seed, self.shinlen,self.mode)
        self.sigDict = {}
        self.bandDicts = {}

        self._init_bandDicts()

        if sigDict is not None:
            try:
                self.sigDict = pickle.load(open(sigDict, "rb"))
                self._buildBands()
            except (OSError, IOError) as e:
                raise ValueError("Could not load signature dictionary with name %s" % sigDict)

    def _init_bandDicts(self):
        for i in range(self.b):
            self.bandDicts[i] = {}

    def addDoc(self,key,content):
        self.sigDict[key] = self.minHash.signature(content)
        self.addBand(key,self.sigDict[key])

    def buildSignatures(self, docs):
        for key,val in tqdm(docs.items()):
            self.addDoc(key,val)
            
    def makeDump(self, fileName):
        pickle.dump(self.sigDict, open(fileName, "wb" ) )

    
    def addBand(self,key,val):
        for i in range(self.b):
            self.bandDicts[i]
            #Tuple is used because lists can not be used as keys
            bandKey = tuple(val[int(self.rows*i):int(self.rows*(i+1))])
            bandValue = key
            if bandKey not in self.bandDicts[i]:
                self.bandDicts[i][bandKey] = [bandValue]
            else:
                self.bandDicts[i][bandKey].append(bandValue)


    #Compute candidates to a signature
    def computeCandidates(self, sig):
        cand = set()
        for i in range(self.b):
            sigKey = tuple(sig[int(self.rows*i):int(self.rows*(i+1))])
            if sigKey in self.bandDicts[i]:
                cand.update(self.bandDicts[i][sigKey])
        return cand

    #Computes the similarity of a document to the candidates
    def compCandSimilarity(self, signature, cands, key=None):
        measures = []
        for cand in cands:
            if not (cand == key):
                simi = self._estJacard(signature,self.sigDict[cand])
                if (simi >= self.threshold):
                    measures.append([simi,cand])
        return measures

    def findSimilarDocuments(self,content):
        signature = self.minHash.signature(content)
        cands = self.computeCandidates(signature)
        return self.compCandSimilarity(signature,cands)


    def computeInternalSimilarities(self):
        sims = []
        for document,signature in list(self.sigDict.items()):
            candidates = self.computeCandidates(signature)

            measures = self.compCandSimilarity(signature,candidates,document)
            
            for measure in measures:
                if [measure[0],measure[1],document] not in sims:
                    sims.append([measure[0],document,measure[1]])
        sims.sort(key=lambda x: float(x[0]))
        return sims

    # Util functions
    def _buildBands(self):
        for key, value in self.sigDict.items():
            self.addBand(key,value)

    def _jacard(self,doc1,doc2):
        a = set(self.sigDict[doc1])
        b = set(self.sigDict[doc2])

        return float(len(a & b)) / len(a | b)

    def _estJacard(self,signature1,signature2):
        a = set(signature1)
        b = set(signature2)

        return len(a & b)/self.k