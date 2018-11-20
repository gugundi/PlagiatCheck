def LSH(sig_Dict, b, rows):
    #Build dictionary for each band
    bandDicts = {}
    for i in range(b):
        bandDict = {}
        for key, value in sig_Dict.items():
            #Tuple is used because lists can not be used as keys
            bandKey = tuple(value[int(rows*i):int(rows*(i+1))])
            bandValue = key
            if bandKey not in bandDict:
                bandDict[bandKey] = [bandValue]
            else:
                bandDict[bandKey].append(bandValue)
        bandDicts[i] = bandDict
    return bandDicts