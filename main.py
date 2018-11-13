import articleReader

dictionary = articleReader.findArticles("Dataset/wikitext-2/wiki.train.tokens")
print(len(dictionary))
print(dictionary[0].encode(encoding='utf8'))
for x in dictionary:
    print(x)
