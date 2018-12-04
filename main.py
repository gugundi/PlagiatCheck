import articleReader
import os
from lsh import LSH
import itertools
from tqdm import tqdm
import time
import multiprocessing
from multiprocessing import Pool
import sys
import argparse

def stringIsInternal(s):
    if s.lower() == 'true':
        return True
    return False

parser = argparse.ArgumentParser()
parser.add_argument('--k', type=int, default=600,
                    help='Number of hash functions')
parser.add_argument('--b', type=int, default=60,
                    help='Number of bands')
parser.add_argument('--mode', type=str, default='fast',
                    help='Mode of MinHash can be slow or fast')
parser.add_argument("--internal", type=stringIsInternal, nargs='?',
                        const=True, default='false',
                        help="Internal Wikipedia similarities")
parser.add_argument('--filePath', type=str, default=None,
                    help='Filepath for file to compare')
args = parser.parse_args()

def wikiParallel(MinHashMode=None):
    lsh = LSH(mode=MinHashMode, k=args.k, b=args.b)
    last_time = False
    j = 0
    start = time.time()
    total_file_time = 0
    testTitleDict = {}

    pool = Pool()
    while not last_time:
        filetimestart = time.time()
        articleDict, titleDict, last_time = articleReader.findArticles("Dataset/wikitext-103/wiki.train.tokens", j)
        testTitleDict.update(titleDict)

        total_file_time += time.time() - filetimestart
        iters = itertools.islice(articleDict.items(),None)
        for key,val in tqdm(pool.imap_unordered(lsh.addDocParallel,iters,len(articleDict)//16)),total=len(articleDict)):
            lsh.sigDict[key] = val
        j += 1
     
    lsh._buildBands()

    if not args.internal:
        f = open(args.filePath, 'r')
        # Printing
        print("============================ Time spent loading files: {:3.2f}s =================================".format(total_file_time))
        print("======================================== LSH stats ===========================================")
        print("||   Mode: {:7s}  |   k: {:4.0f}   |   Shingle-Length: {:2.0f}   |   Bands: {:2.0f}   |   Time: {:4.0f}s  ||".format(lsh.mode,lsh.k,lsh.shinlen,lsh.b,time.time() - start))
        print("==============================================================================================")
        start = time.time()
        print("====================================== LSH similarity ========================================")
        sims = lsh.findSimilarDocuments(f.read())
        for sim in sims: print("|| Sim: {:05.3f} | Cand: {:30.30s} ||".format(sim[0],testTitleDict[sim[1]]))
        print("========================================== Stats =============================================")
        print("||      Sims over threshold {:1.2f}: {:2.0f}         |                   Time: {:2.3f}                ||".format(lsh.threshold,len(sims),time.time() - start))
        print("==============================================================================================")
    else:
        # Printing
        print("============================ Time spent loading files: {:3.2f}s =================================".format(total_file_time))
        print("======================================== LSH stats ===========================================")
        print("||   Mode: {:7s}  |   k: {:4.0f}   |   Shingle-Length: {:2.0f}   |   Bands: {:2.0f}   |   Time: {:4.0f}s  ||".format(lsh.mode,lsh.k,lsh.shinlen,lsh.b,time.time() - start))
        print("==============================================================================================")
        start = time.time()
        print("====================================== LSH similarity ========================================")
        sims = lsh.computeInternalSimilarities()
        for sim in sims: print("|| Sim: {:05.3f} | Doc: {:31.31s} | Cand: {:30.30s} ||".format(sim[0],testTitleDict[sim[1]],testTitleDict[sim[2]]))
        print("========================================== Stats =============================================")
        print("||      Sims over threshold {:1.2f}: {:2.0f}         |                   Time: {:2.3f}                ||".format(lsh.threshold,len(sims),time.time() - start))
        print("==============================================================================================")

if __name__ == '__main__':
    wikiParallel(MinHashMode=args.mode)
