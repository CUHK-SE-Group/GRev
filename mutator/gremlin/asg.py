import random

class ASG:
    def __init__(self, n): 
        self.n = n
        self.m = 0
        self.VisitedNodes = set()
        self.used_node = set()
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
        self.VisitedNodes.add(u)
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
        
        if depth > 0: return res
        
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
        root_node = "n" + str(random.randint(1, self.n))
        self.VisitedNodes.add(root_node)

        res_string = ".match("
        while len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
            res = "__"
            avail_nodes = []
            for node in self.VisitedNodes: 
                if node not in self.DeletedNodes: 
                        avail_nodes.append(node)

            start_id = random.choice(avail_nodes)
            res = res + self.traversal(start_id, 0)
            res_string = res_string + res
            if len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
                res_string = res_string + ", "
        res_string = res_string + ")"
        return res_string


    def traversal_without_match(self, u, depth):
        self.VisitedNodes.add(u)
        constrains = self.__sample_constrains(u)
        
        res = constrains
        if depth > 0: res += constrains
        
        if u in self.used_node:
            if depth == 0: res += '.select("' + u + '")'
            else: res += '.where(eq("' + u + '"))'
        else:
            self.used_node.add(u)
            res += '.as("' + u + '")'

        if depth == 0: res += constrains
        
        avail_edges = []
        for edge in self.edges[u]:
            if edge["id"] not in self.DeletedEdges:
                avail_edges.append(edge)

        length = len(avail_edges)
        if length == 0:
            if len(self.constrains[u]) == 0:
                self.DeletedNodes.add(u)
            return res
        
        if depth > 0: return res
        
        if depth == 0 and random.randint(0, length * 3) == 0:
            return res
        
        go = random.choice(avail_edges)
        res = res + go["content"]
        self.DeletedEdges.add(go["id"])
        res = res + self.traversal_without_match(go["v"], depth + 1)

        if length == 1 and len(self.constrains[u]) == 0:
            self.DeletedNodes.add(u)

        return res

    def to_string_without_match(self):
        root_node = "n" + str(random.randint(1, self.n))
        self.VisitedNodes.add(root_node)

        res_string = ""
        while len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
            res = ""
            avail_nodes = []
            for node in self.VisitedNodes: 
                if node not in self.DeletedNodes: 
                        avail_nodes.append(node)

            start_id = random.choice(avail_nodes)
            res = res + self.traversal_without_match(start_id, 0)
            res_string = res_string + res
            # if len(self.DeletedEdges) < self.m or len(self.DeletedNodes) < self.n:
            #     res_string = res_string + ", "

        res_string += '.select('
        for v in self.used_node:
            res_string += '"' + v + '"'
            res_string += ', '
        
        res_string = res_string.rstrip(", ") + ')'
        return res_string



