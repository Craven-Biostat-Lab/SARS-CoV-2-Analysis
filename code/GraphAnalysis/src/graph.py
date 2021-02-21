import tkinter as tk
import threading, math
from . import get as get

class Graph():
    def __init__(self):
        self.nodes = {}
    
    def buildGraph(self, a, b):
        # update identifier a
        if not self.nodes.get(a): 
            self.nodes[a] = {b: 1}
        else: 
            if not self.nodes[a].get(b):
                self.nodes[a][b] = 1
            else:
                self.nodes[a][b] += 1

        if not self.nodes.get(b): 
            self.nodes[b] = {a: 1}
        else: 
            if not self.nodes[b].get(a):
                self.nodes[b][a] = 1
            else:
                self.nodes[b][a] += 1

def graphData(d, s, ds, t, c, b, p):
    # d: Data object
    # s: selected identifier
    # ds: max degrees of separation
    # t: text box to output results
    # c: 1 or 0 as to whether or not we arrange alphabetically
    # b: the Button object

    if s == "": return

    ignoreHyphen = True
    ignoreDuplicates = True
    ignoreDuplicateViral = True

    TABSIZE = 14
    b["state"] = "disabled"
    t.delete(1.0, tk.END)
    s = s.lower().strip() # normalize to lower case
    ds = int(ds)

    d.selected = s
    d.used.add(s)
    d.disp = "## ONE DEGREE OF SEPARATION:\n"
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
            d.interactions.append([s, key, "human-human"])
            d.used.add(key)
        
        if c == 1: layer1.sort()
        
        for i, term in enumerate(layer1):
            d.disp += f"{term}\n"
            
            progress = int(math.ceil(((i+1)/(len(layer1)+1))*100))
            if progress % 5 == 0: p["value"] = progress

        # two degrees of separation
        if ds >= 2:
            d.disp += "\n## TWO DEGREES OF SEPARATION:\n"
            layer2 = []
            for prot in d.layers[1]:
                for key in d.graph.nodes[prot].keys():
                    if ignoreDuplicates and prot == key: continue   # ignore when interactorA and interactorB are equal
                    if ignoreHyphen and key == "-": continue        # ignore hyphens
                    if key == s: continue                           # ignore interactions with original s

                    layer2.append(f"{prot}\t>>\t{key}".expandtabs(TABSIZE))
                    d.layers[2].add(key)
                    d.interactions.append([prot, key, "human-human"])
                    d.used.add(key)
            
            if c == 1: layer2.sort()

            for i, term in enumerate(layer2):
                d.disp += f"{term}\n"

                progress = int(math.ceil(((i+1)/(len(layer2)+1))*100))
                if progress % 5 == 0: p["value"] = progress

        # regardless of # of layers used, search for viral interactions
        d.disp += "\n## VIRAL INTERACTIONS:\n"
        viral_interactions = []

        for row in get.getRows("src/csv/biogrid_3study_standard_v3.csv")[1:]:
            if not row[0].lower() in d.used: continue

            term = f"{row[0].lower()}\t>>\t{row[3].lower()}".expandtabs(TABSIZE)
            if ignoreDuplicateViral and term in viral_interactions: continue

            viral_interactions.append(term)
            d.interactions.append([row[0].lower(), row[3].lower(), "human-virus"])
        
        if c == 1: viral_interactions.sort()

        for i, term in enumerate(viral_interactions):
            d.disp += f"{term}\n"

            progress = int(math.ceil(((i+1)/(len(viral_interactions)+1))*100))
            if progress % 5 == 0: p["value"] = progress

    except KeyError: d.disp = "Identifier not found."
    t.insert(tk.END, d.disp)

    b["state"] = "normal"
    p["value"] = 0

def startThread(d, s, ds, t, c, b, p):
    # every time this function is called, it creates a new th; meaning that th.start() doesn't
    # call upon the same thread every time. this fixes the runtime error I was encountering.
    # in addition, setting daemon=True means that there aren't threads in the background if the
    # user attempts to exit the program. truly epic
    th = threading.Thread(target=(lambda: graphData(d, s, ds, t, c, b, p)), daemon=True)
    th.start()