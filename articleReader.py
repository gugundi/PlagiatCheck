import re, io

def findArticles(filepath):
    file = io.open(filepath, 'r', encoding='utf8')
    fileContent = file.read()
    # regex = re.compile('(\n\s(?<!=)\s{2}=\s[^=]+=.*)')
    articles = re.split('(\n\s(?<!=)\s{2}=\s[^=]+=.*)', fileContent)
    articleDict = {}
    titleDict = {}

    for x in range(len(articles)):
        if x == 0:
            titleLine = articles[0].split('\n',2)[1]
            title = ''.join(re.findall('[^=]+', titleLine)).encode('utf-8')
            titleDict[x] = title

        # if odd -> title
        if (x & 1):
            # TODO: assign to titleDict
            titleLine = articles[x].split('\n',2)[-1]
            title = ''.join(re.findall('(?<=)[^=]+', titleLine)).encode('utf-8')
            titleDict[int((x+1)/2)] = title
        else:
            # TODO: assign to articleDict
            article = articles[x].encode('utf-8')
            articleDict[int((x)/2)] = article

    return articleDict, titleDict
