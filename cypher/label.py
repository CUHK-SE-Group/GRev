import random
from copy import *
from cypher.schema import GraphSchema

class LabelExpGenerator:
    def __init__(self, G : GraphSchema): 
        self.G = G
        self.Nlabel = []
        self.Rlabel = []
        for i in range(0, self.G.label_num):
            self.Nlabel.append("L" + str(i))
            self.Rlabel.append("T" + str(i))
    
    def gen(self, mytype, simple_version = False):
        #For GDBs other than Neo4j, please use simple_version

        labelset = copy(self.Nlabel) if mytype == "node" else copy(self.Rlabel)
        if simple_version:
            num = random.randint(0, 3)
            labels = random.sample(labelset, num)
            for label in labels: res = res + ":" + str(label)

        labelset.append("%")
        if random.randint(1, 10) == 1: return ""
        res = ":("
        num = random.randint(1, 4)
        leftB = 0
        
        for i in range(0, num):
            while random.randint(1, 3) == 1: res = res + "!"
            if random.randint(1, 3) == 1:
                res = res + "("
                leftB += 1
            while random.randint(1, 3) == 1: res = res + "!"
            res = res + random.choice(labelset)    
            while leftB > 0 and random.randint(1, 3) == 1:
                res = res + ")"
                leftB -= 1
            if i + 1 < num:
                if random.randint(1, 2) == 1:
                    res = res + "&"
                else: res = res + "|"
        
        while leftB > 0:
            res = res + ")"
            leftB -= 1
        return res + ")"

if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    LG = LabelExpGenerator(G)
    print("OK")
            