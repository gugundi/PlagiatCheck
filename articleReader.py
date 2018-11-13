import re

def findArticles(file):
    regex = re.compile("(?<!=)\s=\s[\w+\s]+=")
    articles = regex.split(file)
    return articles
