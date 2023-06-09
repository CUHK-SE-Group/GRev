import random
import string
from mutator.gremlin.schema import GraphSchema
from configs.conf import new_logger, config

class PatternGenerator:
    def __init__(self, G : GraphSchema): self.G = G

    def __Aggregate_Generator(self, my_type, max_length = 10, single_value_only = False):
        P = ""
        for t in range(0, max_length):
            RandomType = random.randint(1, 3)
            if RandomType < 3 or t == max_length - 1:
                # Case1: Generate a aggreagate and return
                _RandomType = random.randint(1, 3)
                if _RandomType < 3:
                    selected_property = list(random.sample(self.G.property_set, 1))[0]
                    type_property = self.G.Type[selected_property]
                    P = P + ".values(" + '"' + selected_property + '"' + ")"
                    
                    if type_property != "string" and type_property != "boolean":
                        aggreagates = ["", ".sum()", ".min()", ".max()", ".mean()"]
                        if single_value_only:
                            index = random.randint(1, 4)
                        else:
                            index = random.randint(0, 4)
                        res_type = self.G.Type[selected_property]
                        if index == 4: res_type = "double"
                        return P + aggreagates[index], res_type
                    else: 
                        aggreagates = ["", ".min()", ".max()"]
                        if single_value_only:
                            index = random.randint(1, 2)
                        else:
                            index = random.randint(0, 2)
                        return P + aggreagates[index], self.G.Type[selected_property]
                else:
                    _RandomType = random.randint(0, 3)
                    aggreagates = [".count()", ".path().count()", \
                        ".simplePath().path().count()", ".cyclicPath().path().count()"]
                   
                    P = P + aggreagates[_RandomType]
                    aggreagates = ["", ".sum()", ".min()", ".max()", ".mean()"]
                    index = random.randint(0, 4)
                    res_type = "count"
                    if index == 0: return P, "count"
                    P = ".flatMap(__" + P + ")"
                    P = P + aggreagates[index]
                    if index == 4: res_type = "double"
                    return P, res_type
            else:
                # Case1: Generate a map
                if my_type == "vertex":
                    motions = [".in()", ".out()", ".both()", ".inE()", ".outE()", ".bothE()"]
                    index = random.randint(0, 5)
                    P = P + motions[index]
                    if index >= 3: my_type = "edge"
                        
                elif my_type == "edge":
                    motions = [".outV()", ".inV()", ".bothV()"]
                    index = random.randint(0, 2)
                    P = P + motions[index]
                    my_type = "vertex"

    def __Sub_predicate_Generator(self, my_type):
        predicates = ["eq", "neq", "lt", "lte", "gt", "gte", "inside", "outside", "between"]
        RandomType = random.randint(0, 8)
        if RandomType < 6: # Case 1: Single Predicate:
            P = predicates[RandomType]
            _RandomType = random.randint(1, 3)
            if my_type == "integer":
                Types = ["integer", "float"]
                index = random.randint(0, 1)
                my_type = Types[index]
            elif my_type == "long" or my_type == "float" or my_type == "double":
                Types = ["integer", "long", "double", "float"]
                index = random.randint(0, 3)
                my_type = Types[index]
            if _RandomType > 1:
                return P + "(" + self.G.Constants.Generate(my_type)[1] + ")"
            else:
                return "not(" + P + "(" + self.G.Constants.Generate(my_type)[1] + ")" + ")"
        else:
            # Case 2: Double-side Predicate:
            P = predicates[RandomType]
            lside, rside = self.G.Constants.Generate(my_type), self.G.Constants.Generate(my_type)
            if lside > rside: lside, rside = rside, lside
            _RandomType = random.randint(1, 3)
            if _RandomType > 1:
                return P + "(" + lside[1] + ", " + rside[1] + ")"
            else:
                return "not(" + P + "(" + lside[1] + ", " + rside[1] + ")" + ")"

    def __Predicate_Generator(self, my_type, maxlength = 5):
        count_not = 0
        P = ""
        length = random.randint(1, maxlength)
        P = P + self.__Sub_predicate_Generator(my_type)
        predicates = ["and(", "or("]

        for i in range(1, length):
            P = P + "."
            index = random.randint(0, 1)
            P = P + predicates[index]
            P = P + self.__Sub_predicate_Generator(my_type)
            P = P + ")"
            if random.randint(0, 3) == 0 and count_not >= 1:
                P = P + ")"
                count_not -= 1
        for i in range(0, count_not):
            P = P + ")"
        return P

    def __Sub_Filter_Generator(self, my_type):
        RandomType = random.randint(1, 5)
        if RandomType == 1: #Case1 hasLabel()
            if my_type == "vertex":
                num = random.randint(1, len(self.G.Vlabelset))
                labels = random.sample(self.G.Vlabelset, min(5, num))
            else:
                num = random.randint(1, len(self.G.Elabelset))
                labels = random.sample(self.G.Elabelset, min(5, num))
            P = "." + "hasLabel("
            for i in range(0, len(labels)):
                if i > 0: P = P + ", "
                P = P + '"' + labels[i] + '"'
            P = P + ")"
            return P
        
        if RandomType == 2: #Case2 has(property, predicate)
            selected_property = list(random.sample(self.G.property_set, 1))[0]
            return ".has(" + '"' + selected_property + '"' + ", " + self.__Predicate_Generator(self.G.Type[selected_property]) + ")"
        if RandomType == 3:
            #Case4 has(property)
            selected_property = list(random.sample(self.G.property_set, 1))[0]
            return ".has(" + '"' + selected_property + '"' + ")"
        if RandomType == 4:
            #Case5 hasNot(property)
            selected_property = list(random.sample(self.G.property_set, 1))[0]
            return ".hasNot(" + '"' + selected_property + '"' + ")"
        if RandomType == 5:
            #Case5 where(aggregate.is(predicate))
            my_aggregate, my_type = self.__Aggregate_Generator(my_type)
            my_aggregate = "__" + my_aggregate
            return ".where(" + my_aggregate + ".is(" + self.__Predicate_Generator(my_type) + "))"

    def GenFilter(self, my_type = "vertex", max_length = 2):
        length = random.randint(1, max_length)
        P = ""
        predicates = [".and(", ".or("]
        index = random.randint(0, 1)
        P = P + predicates[index]
        P = P + "__" + self.__Sub_Filter_Generator(my_type)
        for t in range(1, length):
            P = P + ", __" + self.__Sub_Filter_Generator(my_type)
        return P + ")"

    def GenPath(self):
        if random.randint(1, 5) > 0:
            #Case 1 Vertex -> Vertex with Edge label
            Directions = ["out", "in", "both"]
            inv_Directions = ["in", "out", "both"]
            id = random.randint(0, 2)
            Dir = Directions[id]
            inv_Dir = inv_Directions[id]

            if random.randint(0, 1) > 0:
                #Case 1-1: Vertex -> Vertex no requirement for Edge label

                return "." + Dir + "()", "." + inv_Dir + "()"
            else:
                #Case 1-2: Vertex -> Vertex with Edge labels
                num = random.randint(1, len(self.G.Elabelset))
                labels = random.sample(self.G.Elabelset, num)
                P = "." + Dir + "("
                for i in range(0, len(labels)):
                    if i > 0: P = P + ", "
                    P = P + '"' + labels[i] + '"'
                P = P + ")"
                Q = "." + inv_Dir +  "("
                for i in range(0, len(labels)):
                    if i > 0: Q = Q + ", "
                    Q = Q + '"' + labels[i] + '"'
                Q = Q + ")"

                return P, Q
        else:
            #Case 2 Vertex -> Edge -> Edgefilter -> Vertex
            E_Directions = ["outE", "inE", "bothE"]
            V_Directions = ["inV", "outV", "bothV"]

            inv_E_Directions = ["inE", "outE", "bothE"]
            inv_V_Directions = ["outV", "inV", "bothV"]

            Dirindex = random.randint(0, 2)

            E_Dir = E_Directions[Dirindex]
            V_Dir = V_Directions[Dirindex]
            inv_E_Dir = inv_E_Directions[Dirindex]
            inv_V_Dir = inv_V_Directions[Dirindex]
            
            P = "." + E_Dir
            Q = "." + inv_E_Dir

            if random.randint(1, 2) == 1:
                #Case 2-1: Vertex -> Edge no requirement for Edge label
                P = P + "()"
                Q = Q + "()"
            else:
                #Case 2-2: Vertex -> Edge with Edge labels
                num = random.randint(1, len(self.G.Elabelset))
                labels = random.sample(self.G.Elabelset, num)
                P = P + "("
                Q = Q + "("
                for i in range(0, len(labels)):
                    if i > 0: P = P + ", "
                    P = P + '"' + labels[i] + '"'
                    if i > 0: Q = Q + ", "
                    Q = Q + '"' + labels[i] + '"'

                P = P + ")"
                Q = Q + ")"

            #Append Edge_Filter 
        
            Edge_Filter = self.GenFilter("edge")
            # invP = invP + Edge_Filter + "." + V_InvDir + "()"
            return [P + Edge_Filter + "." + V_Dir + "()", Q + Edge_Filter + "." + inv_V_Dir + "()"]
        
# if __name__ == "__main__":
#     # G = GraphSchema()
#     # G.Graph_Generate()
#     # PG = PatternGenerator(G)
#     # print("OK")

        