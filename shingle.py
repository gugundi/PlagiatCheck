def shingle(q,s):
    tokens = s.split(" ")
    return [tokens[i:i+q] for i in range(0,len(tokens) - q + 1)]