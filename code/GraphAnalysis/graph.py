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