import tkinter as tk
from tkinter import filedialog

from . import graph as gh
from . import get as get

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
        for i in range(2):
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
    rows = get.getRows(s)
    colA = alphaToInt(col1)
    colB = alphaToInt(col2)

    for row in rows[int(ig):]:
        d.graph.buildGraph(row[colA].lower(), row[colB].lower()) # normalize all identifiers to lower case

    f.close()

def outputToCSV(d):
    if d.disp == "" or d.disp == "Identifier not found.": return

    w = open(f"results/{d.selected}_{d.layerCount}layer.csv", 'w')
    w.write(f"interactorA,interactorB,interactionType\n")

    for interaction in d.interactions:
        w.write(f"{interaction[0]},{interaction[1]},{interaction[2]}\n")

    w.close()

def outputToCytoscape(d):
    print("Outputting to Cytoscape.")

def scrollTo(d, e, s, l, txt, scrollbar):
    # d: data object
    # e: StringVar showing error
    # s: symbol to jump to
    # l: layer selected ("First layer", "Second layer", or "Viral interactions")
    # txt: tkinter Text widget to adjust
    # scrollbar: tkinter Scrollbar to adjust

    # comb for the symbol in question
    lines = d.disp.split("\n")[:-1]
    lineCount = len(lines)
    currentLayer = False
    found = False
    position = 0.0

    dropDownTranslations = {
        "## ONE DEGREE OF SEPARATION:": "First Layer",
        "## TWO DEGREES OF SEPARATION:": "Second layer",
        "## VIRAL INTERACTIONS:": "Viral interactions"
    }
    
    # if searching in first layer
    if l == "First layer":
        if s == d.selected: found = True
        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": 
                if i == 0: continue     # skip past first header
                else: break             # stop at the next

            if line.split()[2].strip() == s:
                position = i / lineCount if i != 0 else 0.0
                e.set("")
                found = True
                break

    # if searching in second layer
    elif l == "Second layer":
        if len(d.layers[2]) == 0:   # check if we can even do this
            e.set("Layer out of bounds.")
            return

        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": currentLayer = dropDownTranslations[line]
            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    # if searching in viral layer
    else:
        for i, line in enumerate(lines):
            if len(line.split()) == 0: continue
            term = line.split()[0]
            
            if term == "##": currentLayer = dropDownTranslations[line]
            if currentLayer == l:   # if we're in the right layer,
                if term == s:       # and the first term in the line is the protein we're looking for,
                    position = i / lineCount if i != 0 else 0.0
                    e.set("")
                    found = True
                    break

    if not found:
        e.set("Identifier not found at layer specified.")
        return

    # now scroll to the actual location
    txt.yview_moveto(position - (1 / lineCount))