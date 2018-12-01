import re, io

def findArticles(filepath, chunk):

    # articles = chunk_size/2
    chunk_size = 10000

    file = io.open(filepath, 'r', encoding='utf8')
    fileContent = file.read()
    articles = re.split('(\n\s(?<!=)\s{2}=\s[^=]+=.*)', fileContent)
    file.close()

    first_chunk = False
    last = False
    if len(articles) < (chunk+1)*chunk_size:
        last = True

    if chunk == 0:
        first_chunk = True
        articles = articles[0:chunk_size+1]
    else:
        articles = articles[chunk*chunk_size+1:(chunk+1)*chunk_size]

    articleDict = {}
    titleDict = {}

    for x in range(len(articles)):
        if x == 0 and first_chunk:
            titleLine = articles[0].split('\n',2)[1]
            title = ''.join(re.findall('[^=]+', titleLine))
            titleDict[x+chunk*(chunk_size)] = title

        # if odd -> title
        if (x & first_chunk and first_chunk):
            # TODO: assign to titleDict
            titleLine = articles[x].split('\n',2)[-1]
            title = ''.join(re.findall('(?<=)[^=]+', titleLine))
            #print(titleLine)
            titleDict[int((x+1+chunk*(chunk_size))/2)] = title

        elif (not (x % 2) and (not first_chunk)):
            titleLine = articles[x].split('\n',2)[-1]
            title = ''.join(re.findall('(?<=)[^=]+', titleLine))
            #print(titleLine)
            titleDict[int((x+1+chunk*(chunk_size))/2)] = title

        else:
            # TODO: assign to articleDict
            article = articles[x]
            articleDict[int((x+chunk*(chunk_size))/2)] = article

    return articleDict, titleDict, last
