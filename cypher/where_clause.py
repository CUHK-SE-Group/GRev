import random
from cypher.schema import GraphSchema


class BasicWhereGenerator:
    def __init__(self, G: GraphSchema):
        self.G = G
        self.vars = []

    def __gen_single_exp(self, assigned_v1):
        v1 = random.choice(self.vars) if assigned_v1 is None else assigned_v1
        p1 = random.sample(self.G.prop.keys(), 1)[0]
        if self.G.prop[p1] == "int":
            sgn = random.choice(["=", ">", "<", ">=", "<=", "<>"])
        else:
            sgn = random.choice(["=", "<>"])

        res = v1 + "." + p1 + " " + sgn
        if random.randint(0, 1) == 1:
            c = self.G.CG.gen(self.G.prop[p1])
            res = res + " " + c
        else:
            v2 = random.choice(self.vars)
            p2 = random.choice(self.G.types2prop[self.G.prop[p1]])
            res = res + " " + v2 + "." + p2

        if random.randint(1, 3) == 1:
            res = "NOT " + "(" + res + ")"
        return "(" + res + ")"

    def gen_exp(self, assigned_v1=None):
        num = random.randint(1, 5)
        res = ""
        leftB = 0
        for i in range(0, num):
            while random.randint(1, 3) == 1: res = res + "NOT "
            if random.randint(1, 3) == 1:
                res = res + "("
                leftB += 1
            res = res + self.__gen_single_exp(assigned_v1)
            while leftB > 0 and random.randint(1, 3) == 1:
                res = res + ")"
                leftB -= 1
            if i + 1 < num:
                res = res + " " + random.choice(["AND", "OR"]) + " "
        while leftB > 0:
            res = res + ")"
            leftB -= 1
        return res


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    W = BasicWhereGenerator(G)
    W.vars.append("n")
    W.gen_exp()
    print("OK")
