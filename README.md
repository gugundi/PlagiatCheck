# PlagiatCheck
## Download Dataset
1. Download large dataset from [https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip](https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip) 
2. Unzip and put the file 'wiki.train.tokens' into path ./Dataset/wikitext-103

## Run Internal Similarities
1. Run the command: python main.py --internal True

## Run Similarities of Test File
1. Run the command: python main.py --filePath ./Dataset/RussianMonitorLatnik.txt

### Using Existing Signature Matrix
1. Run above commands with the argument: --sigDict sigDict.p
The existing signature matrix has been computed with default arguments

## Command Line Arguments
* [--k K] Number of hashfunctions in MinHash. Default: 600
* [--b B] Number of bands in LSH. Default: 100
* [--q Q] Shingle length. Default: 4
* [--threshold THRESHOLD] Minimum similarity. Default: 0.4
* [--seed SEED] Seed for hashfunctions. Default: 1
* [--chunkSize CHUNKSIZE] Size of data chunk processed at a time: Default: 5000
* [--mode MODE] Mode of MinHash computation. Can be 'slow' or 'fast'. Default 'fast'
* [--internal [INTERNAL]] Compute internal similarities. Can be 'true' or 'false'. Default 'false' 
* [--makeDump MAKEDUMP] File name of signature matrix dump file. If specified a dump file will be made with the file name. Default: None
* [--filePath FILEPATH] Path to file to compute similarities to. 
* [--sigDict SIGDICT] File name of signature matrix dump file to be used in computations. If specified the program will use the specified signature matrix. Default None

### Example
python main.py --k 600 --b 100 --mode fast --internal False --makeDump newSigDict.p --filePath ./Dataset/RussianMonitorLatnik.txt
