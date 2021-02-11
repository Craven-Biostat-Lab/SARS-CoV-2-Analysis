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