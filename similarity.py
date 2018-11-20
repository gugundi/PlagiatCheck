def jacard(sig_dic,doc1,doc2):
        a = set(sig_dic[doc1])
        b = set(sig_dic[doc2])

        return float(len(a & b)) / len(a | b)

def estJacard(sig_dic,doc1,doc2,k):
        a = set(sig_dic[doc1])
        b = set(sig_dic[doc2])

        return len(a & b)/k