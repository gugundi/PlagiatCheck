import articleReader
import os
from lsh import LSH
import itertools
from tqdm import tqdm
import time
import multiprocessing
from multiprocessing import Pool

docs = {} #dictionary mapping document id to document contents
max_docs = 100

# read data sets
srcfolder = os.path.dirname(os.path.abspath(__file__))
datafolder = os.path.join(srcfolder, "Dataset/ats_corpus")   # change to ats_corpus for large data set

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

def atsCorpusTest(docDict=docs,MinHashMode=None):
    lsh = LSH(mode=MinHashMode,threshold=0.2)
    #lsh.buildSignatures(docDict)
    start = time.time()
    lsh.buildSignaturesParallel(docs)

    # LSH
    print("======================================== LSH stats ===========================================")
    print("||   Mode: {:7s}  |   k: {:4.0f}   |   Shingle-Length: {:2.0f}   |   Bands: {:2.0f}   |    Time: {:4.0f}  ||".format(lsh.mode,lsh.k,lsh.shinlen,lsh.b,time.time() - start))
    print("==============================================================================================")
    start = time.time()
    print("====================================== LSH similarity ========================================")
    sims = lsh.computeInternalSimilarities()
    for sim in sims: print("|| Sim: {:05.3f} | Doc: {:31s} | Cand: {:30s} ||".format(sim[0],sim[1],sim[2]))
    print("========================================== Stats =============================================")
    print("||      Sims over threshold {:1.2f}: {:2.0f}         |                   Time: {:2.3f}                ||".format(lsh.threshold,len(sims),time.time() - start))
    print("==============================================================================================")

def wikiTest(MinHashMode=None):
    lsh = LSH(mode=MinHashMode)
    last_time = False
    j = 0
    start = time.time()
    total_file_time = 0

    pool = Pool()
    while not last_time:
        filetimestart = time.time()
        articleDict, titleDict, last_time = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens", j)
        total_file_time += time.time() - filetimestart
        iters = itertools.islice(articleDict.items(),None)
        for key,val in tqdm(pool.imap_unordered(lsh.addDocParallel,iters),total=len(articleDict)):
            lsh.sigDict[key] = val
        j += 1

    lsh._buildBands()

    # Printing
    print("============================ Time spent loading files: {:3.2f}s =================================".format(total_file_time))
    print("======================================== LSH stats ===========================================")
    print("||   Mode: {:7s}  |   k: {:4.0f}   |   Shingle-Length: {:2.0f}   |   Bands: {:2.0f}   |   Time: {:4.0f}s  ||".format(lsh.mode,lsh.k,lsh.shinlen,lsh.b,time.time() - start))
    print("==============================================================================================")
    start = time.time()
    print("====================================== LSH similarity ========================================")
    sims = lsh.computeInternalSimilarities()
    for sim in sims: print("|| Sim: {:05.3f} | Doc: {:31s} | Cand: {:30s} ||".format(sim[0],sim[1],sim[2]))
    print("========================================== Stats =============================================")
    print("||      Sims over threshold {:1.2f}: {:2.0f}         |                   Time: {:2.3f}                ||".format(lsh.threshold,len(sims),time.time() - start))
    print("==============================================================================================")


if __name__ == '__main__':
    #atsCorpusTest(MinHashMode="slow")
    #atsCorpusTest(MinHashMode="medium")
    #atsCorpusTest(MinHashMode="fast")
    #wikiTest(MinHashMode="slow")
    wikiTest(MinHashMode="medium")
    wikiTest(MinHashMode="fast")
