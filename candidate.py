
def jacard(sig_dic,doc1,doc2):
    a = set(sig_dic[doc1])
    b = set(sig_dic[doc2])

    return float(len(a & b)) / len(a | b)


def estJacard(sig_dic,doc1,doc2,k):
    a = set(sig_dic[doc1])
    b = set(sig_dic[doc2])

    return len(a & b)/k


#Compute candidates to a signature
def computeCandidates(sig, b, bandDicts, rows):
    cand = set()
    for i in range(b):
        sigKey = tuple(sig[int(rows*i):int(rows*(i+1))])
        if sigKey in bandDicts[i]:
            cand.update(bandDicts[i][sigKey])
    return cand

#Computes the similarity of a document to the candidates
def compCandSimilarity(sic_dic, doc, cands, sim, k):
    measures = []
    for cand in cands:
        if not (cand == doc):
            simi = estJacard(sic_dic,doc,cand,k)
            if (simi >= sim):
                measures.append([simi,doc,cand])
    return measures