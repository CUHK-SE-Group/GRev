import random

class ASG:
    def __init__(self, n): 
        self.n = n
        self.m = 0
        self.DeletedEdges, self.DeletedNodes = set(), set()
        self.constrains, self.edges = dict(), dict()
        for i in range(0, n): 
            self.edges["n"+str(i+1)] = []
            self.constrains["n"+str(i+1)] = set()
             
    def addedge(self, x, y, in_path, rev_path):
        self.m += 1        
        edge1 = {"v": y,
                "content": in_path,
                "id": self.m
                }
        edge2 = {"v": x,
                "content": rev_path,
                "id": self.m
                }
        self.edges[x].append(edge1)
        self.edges[y].append(edge2)
    
    def __sample_constrains(self, u):
        if len(self.constrains[u]) == 0: return ""
        n = random.randint(1, len(self.constrains[u]))
        res = ""
        for i in range(0, n):
            x = random.sample(self.constrains[u], 1)[0]
            self.constrains[u].remove(x)
            res = res + x
        return res

    def traversal(self, u, depth):
        constrains = self.__sample_constrains(u)
        if depth > 0: res = constrains + '.as("' + u + '")' 
        else: res = '.as("' + u + '")' + constrains
        
        avail_edges = []
        for edge in self.edges[u]:
            if edge["id"] not in self.DeletedEdges:
                avail_edges.append(edge)

        length = len(avail_edges)
        if length == 0:
            if len(self.constrains[u]) == 0:
                self.DeletedNodes.add(u)
            return res
        
        if depth > 0 and random.randint(0, length) == 0:
            return res
        if depth == 0 and random.randint(0, length * 3) == 0:
            return res
        
        go = random.choice(avail_edges)
        res = res + go["content"]
        self.DeletedEdges.add(go["id"])
        res = res + self.traversal(go["v"], depth + 1)

        if length == 1 and len(self.constrains[u]) == 0:
            self.DeletedNodes.add(u)

        return res

    def to_string(self):
        res_string = ".match("
        while len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
            res = "__"
            avail_nodes = []
            for i in range(1, self.n + 1): 
                if "n" + str(i) not in self.DeletedNodes: avail_nodes.append("n"+str(i))
            start_id = random.choice(avail_nodes)
            res = res + self.traversal(start_id, 0)
            res_string = res_string + res
            if len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
                res_string = res_string + ", "
        res_string = res_string + ")"
        return res_string




