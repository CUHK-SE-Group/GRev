import random
from cypher.ngql.schema import GraphSchema


class BasicWhereGenerator:
    def __init__(self, G: GraphSchema):
        self.G = G
        self.vars = []

    def __gen_single_exp(self, assigned_v1):
        v1 = random.choice(self.vars) if assigned_v1 is None else assigned_v1
        p1_idx = self.G.get_random_prop_idx()
        p1 = self.G.get_prop_name(p1_idx)
        sgn = random.choice(["==", ">", "<", "!="])

        type = self.G.get_prop_type(p1_idx)

        res = v1 + "." + p1 + " " + sgn
        if random.randint(0, 1) == 1:
            c = self.G.CG.gen(type)
            res = res + " " + c
        else:
            v2 = random.choice(self.vars)
            p2_idx = self.G.get_random_prop_idx_of_type(type)
            p2 = self.G.get_prop_name(p2_idx)
            assert self.G.get_prop_type(p2_idx) == type
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
    for _ in range(50):
        print(W.gen_exp())
    print("OK")
