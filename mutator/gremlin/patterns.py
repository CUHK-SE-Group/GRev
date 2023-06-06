import random
from mutator.gremlin.asg import ASG
from mutator.gremlin.schema import GraphSchema
from mutator.gremlin.generator import PatternGenerator
from configs.conf import new_logger, config

class NodePattern:
    def __init__(self, id : str, filters : str, in_path : str, rev_path : str):
        self.id = id
        self.constrains = filters
        self.in_path = in_path
        self.rev_path = rev_path
    
class GraphPattern:
    def __init__(self, PG : PatternGenerator, patterns = []):
        self.PG = PG
        self.n = 0
        self.patterns = patterns
    
    def GetNode(self):
        if random.randint(1, self.n + 1) > self.n / 2:
            self.n += 1
            return "n" + str(self.n)
        else:
            return "n" + str(random.randint(1, self.n))
        
    def GenChain(self):
        len, res = random.randint(2, 5), []
        for i in range(0, len):
            id = self.GetNode()
            if random.randint(0, 3) == 0: filters = self.PG.GenFilter()
            else: filters = ""
            if i == 0: in_path, rev_path = "__", "__"
            else: in_path, rev_path = self.PG.GenPath()
            res.append(NodePattern(id, filters, in_path, rev_path))
        return res

    def GenPatterns(self):
        self.n, self.patterns = 0, []
        len = random.randint(1, 5)
        for i in range(0, len): self.patterns.append(self.GenChain())
    
    def to_asg(self):
        #TODO Convert a pattern class to an ASG (list<list> -> graph)
        target_asg = ASG(self.n)
        for pattern in self.patterns:
            for j in range(0, len(pattern)):
                node = pattern[j]
                if node.constrains != "": target_asg.constrains[node.id].add(node.constrains)
                if j < len(pattern) - 1:
                    _node = pattern[j+1]
                    target_asg.addedge(node.id, _node.id, _node.in_path, _node.rev_path)
        return target_asg


    def to_string(self):
        res = ".match("
        for i in range(0, len(self.patterns)):
            pattern, chain = self.patterns[i], ""
            for j in range(0, len(pattern)):
                node = pattern[j] 
                chain = chain + node.in_path
                chain = chain + node.constrains
                chain = chain + '.as("' + node.id + '")' 
                # if j < len(pattern) - 1: chain = chain + "."
                
            res = res + chain
            if i < len(self.patterns) - 1: res = res + ", "
            else: res = res + ")"
        return res


# if __name__ == "__main__":
#     # G = GraphSchema()
#     # G.Graph_Generate()
#     # PG = PatternGenerator(G)
#     # Pattern = GraphPattern(PG)
#     # Pattern.GenPatterns()
#     # asg = Pattern.to_asg()
#     # print("OK")