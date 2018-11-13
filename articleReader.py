import re

def findArticles(filepath):
    file = open(filepath, 'r')
    fileContent = file.read()
    regex = re.compile('(?<!=)\s=\s[\w+\s]+=')
    articles = regex.split(fileContent)
    return articles
