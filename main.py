import articleReader

articles = articleReader.findArticles("Dataset\wikitext-2\wiki.train.txt")

for article in articles:
    print(article)
