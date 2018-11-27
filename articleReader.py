import re, io

def findArticles(filepath, chunk):
    file = io.open(filepath, 'r', encoding='utf8')
    fileContent = file.read()
    articles = re.split('(\n\s(?<!=)\s{2}=\s[^=]+=.*)', fileContent)
    first_chunk = False
    last = False
    if len(articles) < (chunk+1)*200:
        last = True
    try:
        if chunk == 0:
            first_chunk = True
            articles = articles[0:201]
        else:
            articles = articles[chunk*200+1:(chunk+1)*200]
    except (OSError, IOError) as e:
        articles = articles[chuck*200+1:]
        last = True
        raise ValueError("Could not load signature dictionary with name %s" % sigDict)

    articleDict = {}
    titleDict = {}

    for x in range(len(articles)):
        if x == 0 and first_chunk:
            titleLine = articles[0].split('\n',2)[1]
            title = ''.join(re.findall('[^=]+', titleLine))
            titleDict[x] = title

        # if odd -> title
        if (x & first_chunk):
            # TODO: assign to titleDict
            titleLine = articles[x].split('\n',2)[-1]
            title = ''.join(re.findall('(?<=)[^=]+', titleLine))
            titleDict[int((x+1)/2)] = title
        else:
            # TODO: assign to articleDict
            article = articles[x]
            articleDict[int((x)/2)] = article

    file.close()
    return articleDict, titleDict, last
