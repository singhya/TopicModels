def readFiles(fileName, vocabFileName):
    CR = {}
    doc = []
    with open(vocabFileName) as f:
        CR["vocab"] = [line.rstrip() for line in f]
    with open(fileName) as f:
        doc = f.readlines()
    CR["doc"] = []
    for i,x in enumerate(doc):
        y = x.split()
        ls = []
        for word in y:
            w = int(word.strip())
            ls.append(w)
        CR["doc"].append(ls)
        if(i>3000):
            break
    return CR
