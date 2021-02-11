def getRows(filename):
    f = open(filename, 'r', encoding="utf8")
    ret = []
    for line in f:
        try: ret.append(line.split(','))
        except UnicodeEncodeError: continue
    f.close()
    return ret
    
def getCols(rows):
    ret = [[] for entry in rows[0]]
    for row in rows:
        for i, entry in enumerate(row):
            ret[i].append(entry)
    return ret