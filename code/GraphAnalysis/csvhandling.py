import tkinter as tk
from tkinter import filedialog

import graph as gh

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

def alphaToInt(a):
    if a.isnumeric():
        return int(a)

    ret = 0
    diff = 65 if a.isupper() else 97

    letters = {}
    for i in range(26):
        letters[chr(diff+i)] = i
    if len(a) == 1: return letters[a]
    deg = 1
    for c in a[::-1]:
        ret += deg * letters[c]
        deg *= 26
    
    return ret + 26

class Data():
    def __init__(self):
        self.name = ""
        self.graph = gh.Graph()
        self.disp = ""
        self.selected = ""
        self.interactions = []
        self.used = set()

        self.layerCount = 1
        self.layers = {}
        for i in range(5):
            self.layers[i+1] = set()

    def set(self, s):
        self.name = s

    def get(self):
        return self.name

def getFilename(f):
    ret = ""
    for ch in f[::-1]:
        if ch == '/': break
        ret = ch + ret
    return ret

def askForFile(S, a):
    filename =  filedialog.askopenfilename(
        initialdir = ".",
        title = "Select file",
        filetypes = (("comma-separated values","*.csv"), ("all files","*.*"))
    )

    if (filename[-4:] == ".csv"):
        S.set(getFilename(filename))
        a.set(filename)

    else:
        S.set("Invalid file.")

def extractData(s, col1, col2, ig, d):
    # s: filename
    # col1: interactor column 1
    # col2: interactor column 2
    # ig: ignore this many rows
    # d: Data object

    f = open(s, 'r')
    rows = getRows(s)
    colA = alphaToInt(col1)
    colB = alphaToInt(col2)

    for row in rows[int(ig):]:
        d.graph.buildGraph(row[colA].lower(), row[colB].lower()) # normalize all identifiers to lower case

    f.close()

def graphData(d, s, ds, t, c):
    # d: Data object
    # s: selected identifier
    # ds: max degrees of separation
    # t: text box to output results
    # c: 1 or 0 as to whether or not we arrange alphabetically
    # p: please wait notification

    ignoreHyphen = True
    ignoreDuplicates = True

    TABSIZE = 14
    t.delete(1.0, tk.END)
    s = s.lower().strip() # normalize to lower case
    ds = int(ds)

    d.selected = s
    d.used.add(s)
    d.disp = "ONE DEGREE OF SEPARATION:\n"
    d.layerCount = ds
    
    try:
        if d.graph.nodes == {}:
            return

        elif not d.graph.nodes.get(s):
            t.insert(tk.END, "Identifier not found.")
            return

        # one degree of separation
        layer1 = []
        for key in d.graph.nodes[s].keys():
            if ignoreHyphen and key == "-": continue

            layer1.append(f"{s}\t>>\t{key}".expandtabs(TABSIZE))
            d.layers[1].add(key)
            d.interactions.append([s, key])
            d.used.add(key)
        if c == 1: layer1.sort()
        
        for term in layer1:
            d.disp += f"{term}\n"

        # two degrees of separation
        if ds >= 2:
            d.disp += "\nTWO DEGREES OF SEPARATION:\n"
            layer2 = []
            for prot in d.layers[1]:
                for key in d.graph.nodes[prot].keys():
                    if ignoreDuplicates and prot == key: continue   # ignore when interactorA and interactorB are equal
                    if ignoreHyphen and key == "-": continue        # ignore hyphens
                    if key == s: continue                           # ignore interactions with original s

                    layer2.append(f"{prot}\t>>\t{key}".expandtabs(TABSIZE))
                    d.layers[2].add(key)
                    d.interactions.append([prot, key])
                    d.used.add(key)
            if c == 1: layer2.sort()

            for i, term in enumerate(layer2):
                d.disp += f"{term}\n"

    except KeyError: d.disp = "Identifier not found."
    t.insert(tk.END, d.disp)

def outputToCSV(d):
    if d.disp == "" or d.disp == "Identifier not found.": return

    w = open(f"results/{d.selected}_{d.layerCount}layer.csv", 'w')
    w.write(f"interactorA,interactorB,interactionType\n")

    for interaction in d.interactions:
        w.write(f"{interaction[0]},{interaction[1]},human-human\n")

    for row in getRows("csv/biogrid_3study_standard_v3.csv")[1:]:
        if not row[0].lower() in d.used: continue
        w.write(f"{row[0].lower()},{row[3].lower()},human-virus\n")

    w.close()

def outputToCytoscape(d):
    print("Outputting to Cytoscape.")

"""
represent edges in different layers of connectivity as 
node1 -> node2, both in output and behind the scenes.
hold this edge as either human-human or human-viral.
then output this as csv, with columns:

interactorA     interactorB     interactionType
"""