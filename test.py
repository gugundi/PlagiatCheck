import articleReader
import similarity_exercise

# Test prints all the titles and the first three articles
def articleReaderTest():
    articleDict, titleDict = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens")

    print(str(articleDict[4]))
    print(str(titleDict[4]))

# articleReaderTest()
articleDict, titleDict = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens")
similarity_exercise.signatures(articleDict)
