import articleReader
import similarity_exercise
from similarity_exercise import *

# Test prints all the titles and the first three articles
def articleReaderTest():
    articleDict, titleDict = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens")

    print(str(articleDict[4]))
    print(str(titleDict[4]))

q = 3 # length of shingle
k = 100 # number of minhashes
docs = {} #dictionary mapping document id to document contents
min_sim = 0.15
b = 20
rows = int(k/b)
bandDicts = {}

# articleReaderTest()
articleDict, titleDict = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens")

def test(articles, rebuildSigDict = False, debug = False):
    # Rebuild flag can be set to force rebuilding the signatures
    if rebuildSigDict:
        sigDict = signatures(articles)
        pickle.dump( sigDict, open( "sigDict.p", "wb" ) )
    else:
        # If rebuild is False, then try and load the model,
        # if it doesnt exist, build it
        try:
            sigDict = pickle.load(open("sigDict.p", "rb"))
        except (OSError, IOError) as e:
            sigDict = signatures(articles)
            pickle.dump(sigDict, open("sigDict.p", "wb"))

    # All debug code should be placed in here
    if debug:
        shingles = [shingle(q,articles[article]) for article in articles]
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
    sims = similar(sigDict, articles, k, min_sim)

    for sim in sims: print("| Sim: {:05.3f}   | Doc1: {:30s} | Doc2: {:30s} |".format(sim[0],str(sim[1]),str(sim[2])))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))
    print("")

    # LSH
    start = time.time()
    print("====================================== LSH similarity ========================================")
    lsh_sims = lsh_similar(sigDict,articles,q,k,b,min_sim)
    for sim in lsh_sims: print("| Sim: {:05.3f}   | Doc: {:31s} | Cand: {:30s} |".format(sim[0],sim[1],sim[2]))
    print("--------------------------------------- time {:2.3f}s ------------------------------------------".format(time.time() - start))

test(articleDict, rebuildSigDict = False, debug = True)
