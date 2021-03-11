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

def graphData(d, s, ds, ns, t, c, nt, b, p):
    # d: Data object
    # s: selected identifier
    # ds: max degrees of separation
    # ns: max neighbors from node
    # t: text box to output results
    # c: 1 or 0 as to whether or not we arrange alphabetically
    # nt: 1 or 0 as to whether or not we limit the home node
    # b: the Button object

    if s == "": return

    ignoreHyphen = True
    ignoreDuplicates = True
    ignoreDuplicateViral = True

    TABSIZE = 14
    b["state"] = "disabled" # if this doesn't update fast enough, update it further down the line when we know we're good
    t.delete(1.0, tk.END)
    s = s.lower().strip() # normalize to lower case

    # resetting everything in d
    d.selected = s
    d.used = set()
    d.used.add(s)
    d.disp = "## LAYER 1:\n" # this also resets d.disp
    d.layerCount = ds
    d.layers = {}
    d.interactions = []
    d.headLimited = nt
    
    try:
        if d.graph.nodes == {}:
            return

        elif not d.graph.nodes.get(s):
            t.insert(tk.END, "Identifier not found.")
            b["state"] = "active"
            return

        try: 
            ds = int(ds)
            ns = int(ns)
            d.layerCount = ds
            d.neighborCount = ns
            if ds < 1: raise ValueError

        except ValueError: 
            t.insert(tk.END, "Invalid distance or neighbor value.")
            b["state"] = "active"
            return

        # processing degrees of separation
        layers = []
        for i in range(ds):
            layers.append([])
            d.layers[i] = set()

            if len(layers) == 1:
                for key in d.graph.nodes[s].keys():
                    if ignoreHyphen and key == "-": continue                            # ignore hyphens
                    if nt == 1 and len(list(d.graph.nodes[s].keys())) > ns: continue    # ignore nodes with too many layers

                    layers[i].append(f"{s}\t>>\t{key}".expandtabs(TABSIZE))
                    d.layers[i].add(key)
                    d.interactions.append([s, key, "human", "human", len(layers), "human-human"])
                    d.used.add(key)

            else:
                d.disp += f"\n## LAYER {len(layers)}:\n"
                for prot in d.layers[i-1]: # for every protein in the layer before this newly added one
                    for key in d.graph.nodes[prot].keys():
                        if ignoreDuplicates and prot == key: continue                   # ignore when interactorA and interactorB are equal
                        if ignoreHyphen and key == "-": continue                        # ignore hyphens
                        if key == s: continue                                           # ignore interactions with original s
                        if len(list(d.graph.nodes[prot].keys())) > ns: continue         # ignore nodes with too many neighbors

                        layers[i].append(f"{prot}\t>>\t{key}".expandtabs(TABSIZE))
                        d.layers[i].add(key)
                        d.interactions.append([prot, key, "human", "human", len(layers), "human-human"])
                        d.used.add(key)

            if c == 1: layers[i].sort()

            for i, term in enumerate(layers[i]):
                d.disp += f"{term}\n"

                progress = int(math.ceil(((i+1)/(len(layers[-1])+1))*100))
                if progress % 5 == 0: p["value"] = progress

        # plot viral interactions
        d.disp += "\n## VIRAL INTERACTIONS:\n"
        viral_interactions = []

        for row in get.getRows("src/csv/biogrid_3study_standard_v3.csv")[1:]:
            if not row[0].lower() in d.used: continue

            term = f"{row[0].lower()}\t>>\t{row[3].lower()}".expandtabs(TABSIZE)
            if ignoreDuplicateViral and term in viral_interactions: continue

            viral_interactions.append(term)
            d.interactions.append([row[0].lower(), row[3].lower(), "human", "virus", len(layers)+1, "human-virus"])
        
        if c == 1: viral_interactions.sort()

        for i, term in enumerate(viral_interactions):
            d.disp += f"{term}\n"

            progress = int(math.ceil(((i+1)/(len(viral_interactions)+1))*100))
            if progress % 5 == 0: p["value"] = progress

    except KeyError: d.disp = "Identifier not found."
    t.insert(tk.END, d.disp)

    b["state"] = "normal"
    p["value"] = 0

def startThread(d, s, ds, ns, t, c, nt, b, p):
    # every time this function is called, it creates a new th; meaning that th.start() doesn't
    # call upon the same thread every time. this fixes the RuntimeError I was encountering.
    # in addition, setting daemon=True means that there aren't threads in the background if the
    # user attempts to exit the program. truly epic
    th = threading.Thread(target=(lambda: graphData(d, s, ds, ns, t, c, nt, b, p)), daemon=True)
    th.start()