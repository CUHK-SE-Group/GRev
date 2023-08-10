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
    
    def GetNode(self, return_old_node = False):
        if return_old_node == True:
            return "n" + str(random.randint(1, self.n))
        
        if random.randint(1, self.n + 1) > self.n / 2:
            self.n += 1
            return "n" + str(self.n)
        else:
            return "n" + str(random.randint(1, self.n))
        
    def GenChain(self):
        #TODO Need to test

        if self.n == 0: start_node = self.GetNode(return_old_node = False)
        else: start_node = self.GetNode(return_old_node = True)
        end_node = self.GetNode(return_old_node = False)
        # if random.randint(0, 1) == 1: 
        #     start_node, end_node = end_node, start_node

        res = []
        if random.randint(0, 10) == 0: filters = self.PG.GenFilter()
        else: filters = ""
        in_path, rev_path = "__", "__"
        res.append(NodePattern(start_node, filters, in_path, rev_path))

        if random.randint(0, 4) == 0: filters = self.PG.GenFilter()
        else: filters = ""
        in_path, rev_path = "", ""
        len = random.randint(1, 5)
        for i in range(0, len):
            _in, _rev = self.PG.GenPath()
            in_path = in_path + _in
            rev_path = _rev + rev_path
        
        res.append(NodePattern(end_node, filters, in_path, rev_path))
        return res

        # len, res = random.randint(2, 5), []
        # for i in range(0, len):
        #     id = self.GetNode()
        #     if random.randint(0, 10) == 0: filters = self.PG.GenFilter()
        #     else: filters = ""
        #     if i == 0: in_path, rev_path = "__", "__"
        #     else: in_path, rev_path = self.PG.GenPath()
        #     res.append(NodePattern(id, filters, in_path, rev_path))
        # return res
        

    def GenPatterns(self):
        #TODO Need to test 
        self.n, self.patterns = 0, []
        len = random.randint(2, 8)
        for i in range(0, len): self.patterns.append(self.GenChain())
    
    def to_asg(self):
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
        #TODO Need to test
        res = ".match("
        for i in range(0, len(self.patterns)):
            pattern, chain = self.patterns[i], ""
            for j in range(0, len(pattern)):
                node = pattern[j] 
                if j == 0:
                    chain = chain + node.in_path
                    chain = chain + '.as("' + node.id + '")' 
                    chain = chain + node.constrains
                else:
                    chain = chain + node.in_path
                    chain = chain + node.constrains
                    chain = chain + '.as("' + node.id + '")' 
                # if j < len(pattern) - 1: chain = chain + "."
                
            res = res + chain
            if i < len(self.patterns) - 1: res = res + ", "
            else: res = res + ")"
        return res
    
    def to_string_without_match(self):
        res = ""
        used_node = set()
        for pattern in self.patterns:
            chain = ""
            for j in range(0, len(pattern)):
                node = pattern[j]
                if node.in_path != "__": chain += node.in_path
                if j > 0: chain += node.constrains
                if node.id in used_node:
                    if j == 0: chain += '.select("' + node.id + '")'
                    else: chain += '.where(eq("' + node.id + '"))'
                else:
                    used_node.add(node.id)
                    chain += '.as("' + node.id + '")'
                if j == 0: chain += node.constrains
            res += chain
        
        res += '.select('
        for v in used_node:
            res += '"' + v + '"'
            res += ', '
        res = res.rstrip(", ") + ')'
        return res
        
if __name__ == "__main__":
    G = GraphSchema()
    G.Graph_Generate()
    PG = PatternGenerator(G)
    Pattern = GraphPattern(PG)
    Pattern.GenPatterns()
    asg = Pattern.to_asg()
    print("OK")

#.as("n2").out("Elabel5", "Elabel10", "Elabel8").in().both().as("n1").select("n1").or(__.where(__.inE().values("prop5").min().is(lt("8HowtrT73uModO14Hoic")))).in("Elabel8", "Elabel2", "Elabel1", "Elabel9", "Elabel4", "Elabel6", "Elabel3").in("Elabel9", "Elabel3", "Elabel7", "Elabel1", "Elabel5", "Elabel10").in("Elabel7", "Elabel2", "Elabel9", "Elabel6").both().in().as("n3").select("n2").both("Elabel10").out().and(__.has("prop3"), __.hasNot("prop7")).as("n4").as("n5").in().in().in("Elabel6", "Elabel10", "Elabel8", "Elabel5").both().where(eq("n1")).select("n3").out().where(eq("n3")).select("n5").both("Elabel4", "Elabel5", "Elabel1", "Elabel10", "Elabel8", "Elabel2", "Elabel3").both().as("n6").select("n2", "n1", "n4", "n3", "n6", "n5")