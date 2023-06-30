import random
from copy import *
from cypher.ngql.schema import GraphSchema


class LabelExpGenerator:
    def __init__(self, G: GraphSchema):
        self.G = G

    def gen(self, mytype, simple_version = False, without_percent_sign = False, without_negation = False, without_and = False):
        chosen = None
        if mytype == "vertex":
            v_idx = random.randint(0, self.G.num_vertices-1)
            chosen = self.G.sample_vertex_props(v_idx)
        elif mytype == "edge":
            e_idx = random.randint(0, self.G.num_edges-1)
            chosen = self.G.sample_edge_props(e_idx)
        else: assert False

        result = ''
        for tag, props in chosen.items():
            result += ":" + tag
            if len(props) > 0:
                result += "{"
                result += ", ".join([f'{prop_name}: {val}' for prop_name, val in props.items()])
                result += "}"
        return result


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    LG = LabelExpGenerator(G)
    for _ in range(5):
        print(LG.gen(mytype="vertex"))
        print(LG.gen(mytype="edge"))
