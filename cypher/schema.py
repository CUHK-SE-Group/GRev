import random
import os
from cypher.constant import ConstantGenerator

def create_folders_if_not_exist(file_path):
    dir_path = os.path.dirname(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

class GraphSchema:
    def __init__(self):
        self.label_num = None
        self.edge_prop_val = None
        self.types2prop = None
        self.node_prop_val = None
        self.prop = None
        self.CG = ConstantGenerator()

    def gen(self, output_file="./cypher/schema/create.log", node_num=30, edge_num=150, prop_num=30,
            label_num=8):
        self.label_num = label_num
        self.prop = dict()
        self.node_prop_val = dict()
        self.edge_prop_val = dict()
        self.types2prop = {
            "int": [],
            "float": [],
            "bool": [],
            "string": []
        }

        types = ["int", "float", "bool", "string"]

        for i in range(0, prop_num):
            self.prop["p" + str(i)] = random.choice(types)
            self.node_prop_val["p" + str(i)] = []
            self.edge_prop_val["p" + str(i)] = []
            self.types2prop[self.prop["p" + str(i)]].append("p" + str(i))

        if not os.path.exists(output_file):
            create_folders_if_not_exist(output_file)
        with open(output_file, "w", encoding="utf-8") as f:
            for i in range(0, node_num):
                statement = "CREATE(n0"
                num = random.randint(0, label_num)
                labels = random.sample(list(range(0, label_num)), num)
                for label in labels:
                    statement = statement + ":L" + str(label)
                statement = statement + "{id : " + str(i)
                num = random.randint(0, prop_num)
                properties = random.sample(list(self.prop.keys()), num)
                for x in properties:
                    statement = statement + ", " + x + " : "
                    y = self.CG.gen(self.prop[x])
                    statement = statement + y
                    self.node_prop_val[x].append(y)
                statement = statement + "});"
                print(statement, file=f)

            for i in range(0, edge_num):
                id0, id1 = random.randint(0, node_num), random.randint(0, node_num)
                statement = "MATCH (n0 {id : " + str(id0) + "}), (n1 {id : " + str(id1) + "}) "
                statement = statement + "MERGE(n0)-["
                num = 1
                labels = random.sample(list(range(0, label_num)), num)
                for label in labels:
                    statement = statement + ":T" + str(label)
                statement = statement + "{id : " + str(i + node_num)
                num = random.randint(0, prop_num)
                properties = random.sample(list(self.prop.keys()), num)
                for prop in properties:
                    statement = statement + ", " + prop + " : "
                    val = self.CG.gen(self.prop[prop])
                    statement = statement + val
                    self.edge_prop_val[prop].append(val)
                statement = statement + "}]->(n1);"
                print(statement, file=f)


if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
