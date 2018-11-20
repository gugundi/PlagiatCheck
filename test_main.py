import pickle
import time
import itertools
import signature
import shingle
import minHash
import lsh_cand_sim
import similarity

def similar(sig_dic, docs, k, min_simi):
    sims = []

    for pair in itertools.combinations(docs.keys(), 2):
        sim = similarity.estJacard(sig_dic,pair[0],pair[1],k)
        if sim > min_simi:
            sims.append([sim,pair[0],pair[1]])

    sims.sort(key=lambda x: float(x[0]))
    return sims

def test(k, min_sim, docs, q, b, rebuildSigDict = False, debug = False):
    # Rebuild flag can be set to force rebuilding the signatures
    if rebuildSigDict:
        #sigDict = signature.signatures(docs,q, k)
        sigDict = signature.fastSignatures(docs,q,k,1)
        pickle.dump(sigDict, open( "sigDict.p", "wb" ) )
    else:
        # If rebuild is False, then try and load the model,
        # if it doesnt exist, build it
        try:
            sigDict = pickle.load(open("sigDict.p", "rb"))
        except (OSError, IOError) as e:
            sigDict = signature.signatures(docs,q, k)
            pickle.dump(sigDict, open("sigDict.p", "wb"))

    # All debug code should be placed in here
    if debug:
        shingles = [shingle.shingle(q,docs[doc]) for doc in docs]
        print("These are the first 5 shingles in first doc:")
        print(shingles[0][:5])

        print("These are the minhashes of these shingles:")
        print(minHash.minhash(shingles[0][:4],2))

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
    lsh_sims = lsh_cand_sim.lsh_similar(sigDict,docs,q,k,b,min_sim)
    for sim in lsh_sims: print("| Sim: {:05.3f}   | Doc: {:31s} | Cand: {:30s} |".format(sim[0],sim[1],sim[2]))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))
