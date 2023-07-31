import random
from copy import *
from cypher.schema import GraphSchema


class LabelExpGenerator:
    def __init__(self, G: GraphSchema):
        self.G = G
        self.Nlabel = []
        self.Rlabel = []
        for i in range(0, self.G.label_num):
            self.Nlabel.append("L" + str(i))
            self.Rlabel.append("T" + str(i))

    def gen(self, mytype, simple_version = False, without_percent_sign = False, without_negation = False, without_and = False):
        # For GDBs other than Neo4j, please use simple_version

        labelset = copy(self.Nlabel) if mytype == "node" else copy(self.Rlabel)
        if simple_version:
            if mytype == "node":
                num = random.randint(0, 3)
            elif mytype == "rel":
                num = random.randint(0, 1)
            else:
                assert False

            labels = random.sample(labelset, num)
            res = ''
            for label in labels:
                res += ":" + label
            return res

        if without_percent_sign == False: labelset.append("%")
        if random.randint(1, 10) == 1: return ""
        res = ":("
        num = random.randint(1, 3)
        if num == 3 and random.randint(1, 3) == 1: num += 1
        leftB = 0

        for i in range(0, num):
            if without_negation == False:
                while random.randint(1, 3) == 1: res = res + "!"
            if random.randint(1, 3) == 1:
                res = res + "("
                leftB += 1
            if without_negation == False:
                while random.randint(1, 3) == 1: res = res + "!"
            res = res + random.choice(labelset)
            while leftB > 0 and random.randint(1, 3) == 1:
                res = res + ")"
                leftB -= 1
            if i + 1 < num:
                if random.randint(1, 2) == 1 and without_and == False:
                    res = res + "&"
                else:
                    res = res + "|"

        while leftB > 0:
            res = res + ")"
            leftB -= 1
        return res + ")"


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    LG = LabelExpGenerator(G)
    print("OK")
