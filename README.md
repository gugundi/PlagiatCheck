# PlagiatCheck
## Dataset
1. Download large dataset from https://s3.amazonaws.com/research.metamind.io/wikitext/wikitext-103-v1.zip
2. Unzip and put into path ./Dataset/wikitext-103 (this folder should contain the three token files)

## Run
1. Run main.py

### Command Line Arguments in Order
1. q
2. k
3. b
4. Minimum similarity
5. testMode

#### Example
python3 main.py 3 100 20 0.15 true
