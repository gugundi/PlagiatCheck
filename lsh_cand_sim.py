import similarity

def lsh_similar(sig_dic, docs, q, k, b, min_simi):
    r = int(k/b)
    bandDicts = []

    # Dictionary for each band
    for ii in range(b):
        bandDict = {}

        # Every signature for every band
        for key,value in sig_dic.items():
            cut = value[ii*r:(ii+1)*r]
            bandkey = tuple(cut)
            if bandkey not in bandDict.keys():
                bandDict[bandkey] = [key]
            else:
                bandDict[bandkey].append(key)
        
        bandDicts.append(bandDict)

 
    # Find candidates for each document
    sims = []
    for document in list(docs.keys()):
        candidates = []
        signature = sig_dic[document]

        for ii in range(b):
            cut = signature[ii*r:(ii+1)*r]
            bandkey = tuple(cut)
            if bandkey not in bandDicts[ii].keys():
                continue
            else:
                candidates.extend(bandDicts[ii][bandkey])
        
        # For each candidate, see if they have a high similarity
        candidates = set(candidates)
        for candidate in candidates:
            if candidate == document:
                continue

            sim = similarity.estJacard(sig_dic, document, candidate,k)
            if sim > min_simi:
                if [sim,candidate,document] not in sims:
                    sims.append([sim,document,candidate])
    sims.sort(key=lambda x: float(x[0]))
    return sims