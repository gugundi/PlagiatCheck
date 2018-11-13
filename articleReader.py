import re, io

def findArticles(filepath):
    file = io.open(filepath, 'r', encoding='utf8')
    fileContent = file.read()
    regex = re.compile('\n\s(?<!=)\s{2}=\s[^=]+=.*')
    articles = regex.split(fileContent)
    dictionary = {}
    for x in range(len(articles)):
        dictionary[x] = articles[x]
    return dictionary
