import random
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
        self.G = PG
        self.n = 0
        self.patterns = patterns
    
    def GetNode(self):
        if random.randomint(1, self.n + 1) > self.n / 2:
            self.n += 1
            return "n" + str(self.n)
        else:
            return "n" + str(random.randomint(1, self.n))
        
    def GenChain(self):
        len, res = random.randomint(2, 8), []
        for i in range(0, len):
            id = self.GetNode()
            filters = self.PG.GenFilter()
            if i == 0: in_path, rev_path = "__.", "__."
            else: in_path, rev_path = self.PG.GenPath()
            res.append(NodePattern(id, filters, in_path, rev_path))
        return res

    def GenPatterns(self):
        self.n, self.patterns = 0, []
        len = random.randomint(1, 5)
        for i in range(0, len): self.patterns.append(self.Getchain())

    def to_string(self):
        res = ".match("
        for i in range(0, len(self.patterns)):
            pattern, chain = self.patterns[i], ""
            for j in range(0, len(pattern)):
                node = pattern[j] 
                chain = chain + node.in_path
                chain = chain + node.constrains
                chain = chain + "as('" + node.id + "')" 
                if j < len(pattern): chain = chain + "."
                
            res = res + chain
            if i < len(self.patterns): res = res + ","
            else: res = res + ")"

        
