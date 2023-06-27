import random
from cypher.schema import GraphSchema
from cypher.where_clause import BasicWhereGenerator
from cypher.label import LabelExpGenerator


class PatternGenerator:
    def __init__(self, G : GraphSchema): 
        self.node_num = 0
        self.edge_num = 0
        self.G = G
        self.where_generator = BasicWhereGenerator(self.G)
        self.label_generator = LabelExpGenerator(self.G)

    def __get_node_name(self):
        if random.randint(1, self.node_num + 1) > self.node_num - 2:
            self.node_num += 1
            self.where_generator.vars.append("n" + str(self.node_num))
            return "n" + str(self.node_num)
        else:
            return "n" + str(random.randint(1, self.node_num))
    
    def __get_rel_name(self):
        self.edge_num += 1
        self.where_generator.vars.append("r" + str(self.edge_num))
        return "r" + str(self.edge_num)
    
    def __gen_node(self, c_property = True): 
        res = "(" + self.__get_node_name()
        #Add labels
        res = res + self.label_generator.gen(mytype ="node")
        if c_property and random.randint(1, 10) == 1:
            num = 1
            if random.randint(1, 5) == 1: num += 1
            res = res + " {"
            props = random.sample(self.G.prop.keys(), num)
            for i in range(0, num):
                p = props[i]
                res = res + p + ": "
                if len(self.G.edge_prop_val[p]) == 0:
                    res = res + self.G.CG.gen(self.G.prop[p])
                else:
                    res = res + random.choice(self.G.edge_prop_val[p])
                if i == 0 and num > 1: res = res + ", "
            res = res + "}"
        return res + ")"

    def __gen_vari(self):
        op = random.randint(1, 4)
        if op == 1:
            # Case1: l <= length <= r
            x = random.randint(0, 15)
            y = random.randint(0, 15)
            if x > y: x, y = y, x
            return "*" + str(x) + ".." + str(y)
        if op == 2:
            #Case2: l <= length
            x = random.randint(0, 15)
            return "*" + str(x) + ".."
        if op == 3:
            #Case3: length <= r
            x = random.randint(0, 15)
            return "*" + ".." + str(x)
        if op == 4:
            #Case4: any length
            return "*"

    def __gen_rel(self, c_property = True, c_where = True, c_variable = True):
        res = "["
        if random.randint(1, 3) == 3: 
            #No varibale relation
            #Add labels
            res = res + self.label_generator.gen(mytype ="rel")
            #Add Constrains on Property
            if c_variable: res = res + " " + self.__gen_vari()
            if c_property and random.randint(1, 10) == 1:
                num = 1
                if random.randint(1, 5) == 1: num += 1
                res = res + " {"
                props = random.sample(self.G.prop.keys(), num)
                for i in range(0, num):
                    p = props[i]
                    res = res + p + ": "
                    if len(self.G.edge_prop_val[p]) == 0:
                        res = res + self.G.CG.gen(self.G.prop[p])
                    else:
                        res = res + random.choice(self.G.edge_prop_val[p])
                    if i == 0 and num > 1: res = res + ", "
                res = res + "}"
        else:
            var = self.__get_rel_name()
            res = res + var
            #Add labels
            res = res + self.label_generator.gen(mytype ="rel")
            #Add Constrains on Property
            if c_property and random.randint(1, 10) == 1:
                num = 1
                if random.randint(1, 5) == 1: num += 1
                res = res + " {"
                props = random.sample(self.G.prop.keys(), num)
                for i in range(0, num):
                    p = props[i]
                    res = res + p + ": "
                    if len(self.G.edge_prop_val[p]) == 0:
                        res = res + self.G.CG.gen(self.G.prop[p])
                    else:
                        res = res + random.choice(self.G.edge_prop_val[p])
                    if i == 0 and num > 1: res = res + ", "
                res = res + "}"
            #Add Constrains on Where
            if c_where and random.randint(1, 5) == 5:
                res = res + " WHERE "
                res = res + self.where_generator.gen_exp(var)
            
        res = res + "]"
        dirs = [("<-","-"), ("-", "->"), ("-", "-")]
        dir = random.choice(dirs)
        return dir[0] + res + dir[1]


    def gen_path(self):
        res = ""
        num = random.randint(1, 6)
        for i in range(0, num):
            res = res + self.__gen_node()
            if i + 1 < num:
                res = res + self.__gen_rel()        
        return res


    def gen_pattern(self):
        num = random.randint(1, 4)
        res = ""
        for i in range(0, num):
            res = res + self.gen_path()
            if i + 1 < num:
                res = res + ", "
        return res
            
        

if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    P = PatternGenerator(G)
    print("OK")