import sys

def intToAlpha(n):
    key = {}
    ret = ""
    for i in range(26):
        key[i] = chr(65+i)
        
    key[-1] = "A"
    if n < 26: return key[n]
    elif n > 26: n += 1
    
    while n > 0:
        ret = key[(n % 26) - 1] + ret
        n = n // 26
    return ret

def getRows(filename):
    f = open(filename, 'r', encoding="utf8")
    ret = []
    for i, line in enumerate(f):
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

def uniqueValsPerCol(col):
    ret = {}
    for entry in col:
        if not ret.get(entry): ret[entry] = 1
        else: ret[entry] += 1
    return ret

def outputAnalysis(filename):
    spacing = 1
    tabsize = 8
    limit = 50
    if len(sys.argv) > 1: limit = int(sys.argv[1])

    rows = getRows(filename)
    cols = getCols(rows[1:]) # [1:] because we skip the header row
    uniq = [uniqueValsPerCol(col) for col in cols]

    w = open("TableAnalysisResults.txt", 'w')
    w.write(f"LIMIT:\t{limit}\n".expandtabs(tabsize))
    w.write("\n"*spacing)
    w.write(f"KEY:\nCOUNT\tENTRY\n".expandtabs(tabsize))
    w.write("\n"*spacing)

    for i, dc in enumerate(uniq):
        st = dict(sorted(dc.items(), key=lambda item: item[1]))
        st = dict(reversed(list(st.items())))

        rowName = rows[0][i] if rows[0][i][-1] != '\n' else rows[0][i][:-1]
        w.write(f"{intToAlpha(i)}\t{rowName}:\n".expandtabs(tabsize))

        if len(list(st.keys())) > limit:
            w.write(f"{len(list(st.keys()))}\tunique entries.\n".expandtabs(tabsize))
        else:
            for key in st.keys():
                try: k = key if key[-1] != '\n' else key[:-1]
                except: pass
                w.write(f"{st[key]}\t{k}\n".expandtabs(tabsize))
        w.write("\n"*spacing)

    w.close()

def main():
    outputAnalysis("csv/semicolon.csv")

if __name__ == "__main__":
    main()