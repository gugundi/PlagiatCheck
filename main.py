import os
import test_main
import sys
import pickle
from signature import fastSignatures


def buildSignatureDict(rebuildSigDict, q, k):
    # Rebuild flag can be set to force rebuilding the signatures
    if rebuildSigDict:
        #sigDict = signature.signatures(docs,q, k)
        sigDict = fastSignatures(docs,q,k,1)
        pickle.dump(sigDict, open( "sigDict.p", "wb" ) )
    else:
        # If rebuild is False, then try and load the model,
        # if it doesnt exist, build it
        try:
            sigDict = pickle.load(open("sigDict.p", "rb"))
        except (OSError, IOError) as e:
            sigDict = fastSignatures(docs,q, k, 1)
            pickle.dump(sigDict, open("sigDict.p", "wb"))
    return sigDict

q = int(sys.argv[1]) # length of shingle
k = int(sys.argv[2]) # number of minhashes
b = int(sys.argv[3])
min_sim = float(sys.argv[4])
testMode = sys.argv[5].lower() == 'true'

rebuildSigDict = False
docs = {} #dictionary mapping document id to document contents
sig_Dict = {}
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

sig_Dict = buildSignatureDict(rebuildSigDict, q, k)

if testMode:
    test_main.test(sig_Dict, k, min_sim, docs, q, b, debug=True)
else:
    print("LOL")
