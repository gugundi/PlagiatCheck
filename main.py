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

def stringToBool(s):
    return s.lower() == 'true' or s.lower() == '1'

parser = argparse.ArgumentParser()
parser.add_argument('--k', type=int, default=600,
                    help='Number of hash functions')
parser.add_argument('--b', type=int, default=60,
                    help='Number of bands')
parser.add_argument('--q', type=int, default=4,
                    help='Length of shingles')
parser.add_argument('--threshold', type=float, default=0.4,
                    help='Treshold for similarity')
parser.add_argument('--seed', type=int, default=1,
                    help='Seed for MinHash')
parser.add_argument('--chunkSize', type=int, default=5000,
                    help='Size of data chunks')
parser.add_argument('--mode', type=str, default='fast',
                    help='Mode of MinHash can be slow or fast')
parser.add_argument("--internal", type=stringToBool, nargs='?',
                        const=True, default='false',
                        help="Internal Wikipedia similarities")
parser.add_argument('--makeDump', type=str, default=None,
                        help="Make dump of signature matrix")
parser.add_argument('--filePath', type=str, default=None,
                    help='Filepath for file to compare')
parser.add_argument('--sigDict', type=str, default=None,
                    help='Signature dict file')
args = parser.parse_args()

def wikiParallel(MinHashMode=None):
    lsh = LSH(mode=MinHashMode, sigDict=args.sigDict, k=args.k, shinlen=args.q, b=args.b, seed=args.seed, threshold=args.threshold)
    last_time = False
    j = 0
    start = time.time()
    total_file_time = 0
    testTitleDict = {}
    chunkSize = args.chunkSize
    if args.sigDict is not None:
        chunkSize = 70000
        
    pool = Pool()
    while not last_time:
        filetimestart = time.time()
        articleDict, titleDict, last_time = articleReader.findArticles("Dataset/wikitext-103/wiki.train.tokens", j, chunkSize)
        testTitleDict.update(titleDict)

        total_file_time += time.time() - filetimestart
        if args.sigDict is None:
            iters = itertools.islice(articleDict.items(),None)
            for key,val in tqdm(pool.imap_unordered(lsh.addDocParallel,iters,len(articleDict)//16),total=len(articleDict)):
                lsh.sigDict[key] = val
        j += 1
    if args.makeDump is not None:
        lsh.makeDump(args.makeDump)
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
