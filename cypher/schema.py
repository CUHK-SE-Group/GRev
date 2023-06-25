import random
from cypher.constant import ConstantGenerator

class GraphSchema:
    def __init__(self): self.CG = ConstantGenerator()

    def gen(self, output_file = "./cypher/schema/create.log", n = 30, m = 150, p = 30, l = 8):        
        self.label_num = l
        self.prop = dict()
        self.nval = dict()
        self.rval = dict()
        self.types2prop = {
            "int" : [], 
            "float" : [],
            "bool" : [],
            "string" : []
        }

        types = ["int", "float", "bool", "string"]
        
        for i in range(0, p): 
            self.prop["p"+str(i)] = random.choice(types)
            self.nval["p"+str(i)] = []
            self.rval["p"+str(i)] = []
            self.types2prop[self.prop["p"+str(i)]].append("p" + str(i))
        
        
        with open(output_file, "w", encoding = "utf-8") as f:
            for i in range(0, n):
                statement = "CREATE(n0"
                num = random.randint(0, l)
                labels = random.sample(list(range(0, l)), num)
                for x in labels:
                    statement = statement + ":L" + str(x)
                statement = statement + "{id : " + str(i)
                num = random.randint(0, p)
                properties = random.sample(self.prop.keys(), num)
                for x in properties:
                    statement = statement + ", " + x + " : "
                    y = self.CG.gen(self.prop[x])
                    statement = statement + y
                    self.nval[x].append(y)
                statement = statement + "});"
                print(statement, file = f)
            
            for i in range(0, m):
                id0, id1 = random.randint(0, n), random.randint(0, n)
                statement = "MATCH (n0 {id : " + str(id0) + "}), (n1 {id : " + str(id1) + "}) "
                statement = statement + "MERGE(n0)-[r"
                num = random.randint(0, l)
                labels = random.sample(list(range(0, l)), num)
                for x in labels:
                    statement = statement + ":T" + str(x)
                statement = statement + "{id : " + str(i + n) 
                num = random.randint(0, p)
                properties = random.sample(self.prop.keys(), num)
                for x in properties:
                    statement = statement + ", " + x + " : "
                    y = self.CG.gen(self.prop[x])
                    statement = statement + y
                    self.rval[x].append(y)
                statement = statement + "}]->(n1);"
                print(statement, file = f)

if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
