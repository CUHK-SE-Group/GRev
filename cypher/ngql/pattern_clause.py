import random
from cypher.ngql.schema import GraphSchema
from cypher.ngql.where_clause import BasicWhereGenerator
from cypher.ngql.label import LabelExpGenerator


class PatternGenerator:
    def __init__(self, G : GraphSchema): 
        self.node_num = 0
        self.edge_num = 0
        self.G = G
        self.where_generator = BasicWhereGenerator(self.G)
        self.label_generator = LabelExpGenerator(self.G)
        self.allow_empty_node_when_no_new_variables = True

    def __get_node_name(self, no_new_variables = False):
        if no_new_variables == False:
            if random.randint(1, self.node_num + 1) > self.node_num - 2:
                self.node_num += 1
                self.where_generator.vars.append("n" + str(self.node_num))
                return "n" + str(self.node_num)
            else:
                return "n" + str(random.randint(1, self.node_num))
        else:
            if random.randint(1, 3) == 1 and self.allow_empty_node_when_no_new_variables == True: return " "
            return "n" + str(random.randint(1, self.node_num))
    
    def __get_rel_name(self):
        self.edge_num += 1
        self.where_generator.vars.append("r" + str(self.edge_num))
        return "r" + str(self.edge_num)
    
    def __gen_node(self, c_property = True, no_new_variables = False): 
        res = "(" + self.__get_node_name(no_new_variables = no_new_variables)
        # Add tags without labels
        if c_property and random.randint(1, 20) == 1:
            res += self.label_generator.gen(mytype="vertex")
        else:
            res += self.label_generator.gen(mytype="vertex", allow_properties=False)
        res += ")"
        return res

    def __gen_vari(self):
        op = random.randint(1, 4)
        if op == 1:
            # Case1: l <= length <= r
            x = random.randint(0, 15)
            y = random.randint(1, 15)
            if x > y: x, y = y, x
            return "*" + str(x) + ".." + str(y)
        if op == 2:
            #Case2: l <= length
            x = random.randint(0, 15)
            return "*" + str(x) + ".."
        if op == 3:
            #Case3: length <= r
            x = random.randint(1, 15)
            return "*" + ".." + str(x)
        if op == 4:
            #Case4: any length
            return "*"

    def __gen_rel(self, c_property = True, c_where = True, c_variable = True, no_new_variables = False):
        res = "["

        if random.randint(1, 3) == 1 or no_new_variables:
            # Without variable names
            if c_variable and random.randint(1, 2) == 1:
                res += self.__gen_vari()
            else:
                res += self.label_generator.gen(mytype="edge", allow_properties=False)
        else:
            res += self.__get_rel_name()
            res += self.label_generator.gen(mytype="edge", allow_properties=False)
            
        res = res + "]"
        dirs = [("<-","-"), ("-", "->"), ("-", "-")]
        dir = random.choice(dirs)
        res = dir[0] + res + dir[1]
        return res


    def gen_path(self, no_new_variables = False, num_lo=1):
        res = ""
        num = random.randint(num_lo, 4)
        for i in range(0, num):
            res = res + self.__gen_node(no_new_variables = no_new_variables)
            if i + 1 < num:
                res = res + self.__gen_rel(no_new_variables = no_new_variables, c_variable=False)
        return res


    def gen_pattern(self, no_new_variables = False):
        if no_new_variables == True: 
            self.allow_empty_node_when_no_new_variables = False
        num = random.randint(2, 4)
        res = ""
        for i in range(0, num):
            res = res + self.gen_path(no_new_variables = no_new_variables, num_lo=2)
            if i + 1 < num:
                res = res + ", "
        
        self.allow_empty_node_when_no_new_variables = True
        return res
            
        

if __name__ == "__main__":
    G = GraphSchema()
    G.gen()
    P = PatternGenerator(G)
    with open ("./mutator/ngql/pattern_sample.in", "w") as f:
        for _ in range(10000):
            print(P.gen_pattern(), file=f)


