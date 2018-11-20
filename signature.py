from tqdm import tqdm
import shingle
import minHash
def signatures(docsDict:dict, k):
    sigDict = {}

    print("Creating signatures")
    for key in tqdm(docsDict.keys()):
        q = 3
        shin = shingle.shingle(q,docsDict[key])
        minh = minHash.minhash(shin,k)
        sigDict[key] = minh
    return sigDict

def docSignature(doc, q, k):
    return minHash.minhash(shingle.shingle(q,doc),k)