import random
from cypher.constant import ConstantGenerator


class GraphSchema:
    def __init__(self):
        self.num_vertices = None
        self.num_edges = None

        self.props = None
        self.vertex_tags = None
        self.edge_tags = None

        self.vertices = None
        self.edges = None

        self.num_labels = None
        self.edge_prop_val = None
        self.types2prop = None
        self.node_prop_val = None
        self.CG = ConstantGenerator()

    @staticmethod
    def mysample(a, nonempty=False):
        if nonempty:
            assert(len(a) > 0)
            num = random.randint(1, len(a))
        else:
            num = random.randint(0, len(a))
        return random.sample(a, num)

    def gen(self, output_file="./cypher/ngql/schema/create.log", num_vertices=30, num_edges=150, num_props=30,
            num_vertex_tags=8, num_edge_tags=18):
        self.num_vertices = num_vertices
        self.num_edges = num_edges

        # 1. Prepare properties
        self.props = [dict()] * num_props
        types = ["int", "float", "bool", "string"]
        for prop_idx in range(num_props):
            self.props[prop_idx] = {
                "name": "p" + str(prop_idx),
                "type": random.choice(types)
            }

        # 2. Prepare tags
        self.vertex_tags = [dict()] * num_vertex_tags
        for vtag_idx in range(num_vertex_tags):
            self.vertex_tags[vtag_idx] = {
                "name": "L" + str(vtag_idx),
                "props": GraphSchema.mysample([_ for _ in range(num_props)])
            }

        self.edge_tags = [dict()] * num_edge_tags
        for etag_idx in range(num_edge_tags):
            self.edge_tags[etag_idx] = {
                "name": "T" + str(etag_idx),
                "props": GraphSchema.mysample([_ for _ in range(num_props)])
            }

        # 3. Prepare vertices and edges
        self.vertices = [dict()] * num_vertices
        # (name, props)
        for v_idx in range(num_vertices):
            cur_tags = GraphSchema.mysample([_ for _ in range(num_vertex_tags)], nonempty=True)
            tag_props = dict()
            for vtag_idx in cur_tags:
                props = GraphSchema.mysample(self.vertex_tags[vtag_idx]["props"])
                prop_vals = dict()
                for prop_idx in props:
                    prop_vals[prop_idx] = self.CG.gen(mytype=self.props[prop_idx]["type"])

                tag_props[vtag_idx] = prop_vals

            self.vertices[v_idx] = {
                "name": "n" + str(v_idx),
                "props": tag_props
            }

        self.edges = [dict()] * num_edges
        # (st, en, props)
        # Note that each edge has exactly one type (edge tag)
        for e_idx in range(num_edges):
            st_idx = random.randint(0, self.num_vertices-1)
            en_idx = random.randint(0, self.num_vertices-1)

            cur_tags = GraphSchema.mysample([_ for _ in range(num_edge_tags)], nonempty=True)
            tag_props = dict()
            for etag_idx in cur_tags:
                props = GraphSchema.mysample(self.edge_tags[etag_idx]["props"])
                prop_vals = dict()
                for prop_idx in props:
                    prop_vals[prop_idx] = self.CG.gen(mytype=self.props[prop_idx]["type"])

                tag_props[etag_idx] = prop_vals

            self.edges[e_idx] = {
                "st": st_idx,
                "en": en_idx,
                "props": tag_props
            }

        with open(output_file, "w", encoding="utf-8") as f:
            # 1. CREATE TAG IF NOT EXISTS [name] (list of parameters)
            for vtag in self.vertex_tags:
                params_list = "(" + ", ".join([f'{self.props[i]["name"]} {self.props[i]["type"]}' for i in vtag["props"]]) + ")"
                statement = "CREATE TAG IF NOT EXISTS " + vtag["name"] + " " + params_list
                print(statement)
                print(statement, file=f)

            # 2. CREATE EDGE IF NOT EXISTS [name] (list of parameters)
            for etag in self.edge_tags:
                param_list = "(" + ", ".join([f'{self.props[i]["name"]} {self.props[i]["type"]}' for i in etag["props"]]) + ")"
                statement = "CREATE EDGE IF NOT EXISTS " + etag["name"] + " " + param_list
                print(statement)
                print(statement, file=f)

            # 3. INSERT VERTEX [tag] (list of parameters) VALUES "[name]" (list of values)
            for v in self.vertices:
                assert len(v["props"]) > 0
                for vtag_idx, cur_props in v["props"].items():
                    assert isinstance(cur_props, dict)
                    params_list = "(" + ", ".join([self.props[i]["name"] for i in cur_props.keys()]) + ")"
                    values_list = "(" + ", ".join([x for x in cur_props.values()]) + ")"
                    statement = "INSERT VERTEX "
                    statement += self.vertex_tags[vtag_idx]["name"] + " "
                    statement += params_list + " "
                    statement += "VALUES" + " "
                    statement += f'"{v["name"]}"' + " : "
                    statement += values_list
                    print(statement)
                    print(statement, file=f)

            # 4. INSERT EDGE [tag] (list of parameters) VALUES "[st_name]"->"[en_name]" (list of values)
            for e in self.edges:
                assert len(v["props"]) > 0
                st_name = self.vertices[e["st"]]["name"]
                en_name = self.vertices[e["en"]]["name"]
                for etag_idx, cur_props in e["props"].items():
                    assert isinstance(cur_props, dict)
                    params_list = "(" + ", ".join([self.props[i]["name"] for i in cur_props.keys()]) + ")"
                    values_list = "(" + ", ".join([x for x in cur_props.values()]) + ")"
                    statement = "INSERT EDGE "
                    statement += self.edge_tags[etag_idx]["name"] + " "
                    statement += params_list + " "
                    statement += "VALUES" + " "
                    statement += f'"{st_name}"->"{en_name}"' + " : "
                    statement += values_list
                    print(statement)
                    print(statement, file=f)

            # 5. Create&rebuild vertex tags
            for vtag in self.vertex_tags:
                statement = "CREATE TAG INDEX IF NOT EXISTS "
                statement += f'{vtag["name"]}_index' + " ON "
                statement += f'{vtag["name"]}()'
                print(statement)
                print(statement, file=f)

            for vtag in self.vertex_tags:
                statement = "REBUILD TAG INDEX "
                statement += f'{vtag["name"]}_index'

            # 6. Create&rebuild edge tags
            for etag in self.edge_tags:
                statement = "CREATE EDGE INDEX IF NOT EXISTS "
                statement += f'{etag["name"]}_index' + " ON "
                statement += f'{etag["name"]}()'
                print(statement)
                print(statement, file=f)

            for etag in self.edge_tags:
                statement = "REBUILD EDGE INDEX "
                statement += f'{etag["name"]}_index'


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
