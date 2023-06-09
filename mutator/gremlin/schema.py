import random
import string
from mutator.gremlin.constant import Constant_Generator
from configs.conf import new_logger, config


class GraphSchema:
    def __init__(self, GDB_header = "g.", output_file = "./mutator/gremlin/schemas/gremlin_schema.log"):
        self.GDB_header = GDB_header
        self.logger = new_logger("logs/gremlin.log")
        self.output_file = open(output_file, "w", encoding = "utf+8")

        self.Vlabelset = set()
        self.Elabelset = set()
        self.property_set = set()
        self.Type = {}
        self.Constants = Constant_Generator()
        self.Vertex2Label = {}
        self.Vertex2Prop = {}
        self.Edge2Label = {}
        self.Edge2Prop = {}
        self.Edge2Ends = {}
        self.label2Vertex = {}
        self.Vlabel2prop = {}
        self.Elabel2prop = {}
        self.Elabel2ST = {}      
    
    def __output_statement(self, statement):
        print(statement, file = self.output_file)

    def __GenerateProp(self, property_num):
        self.property_num = property_num
        for index in range(1, property_num + 1):
            prop_name = f"prop{index}"
            self.property_set.add(prop_name)
            prop_types = ["integer", "double", "string", "long", "float", "boolean"]
            p_index = random.randint(0, 5)
            self.Type[prop_name] = prop_types[p_index]

            if self.GDB_header != "hugegraph.traversal().": continue
            #only for hugegraph

            if prop_types[p_index] == "string":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asText().ifNotExist().create()')
            if prop_types[p_index] == "integer":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asInt().ifNotExist().create()')
            if prop_types[p_index] == "long":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asLong().ifNotExist().create()')
            if prop_types[p_index] == "double":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asDouble().ifNotExist().create()')
            if prop_types[p_index] == "float":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asFloat().ifNotExist().create()')
            if prop_types[p_index] == "boolean":
                self.__output_statement(f'hugegraph.schema().propertyKey("{prop_name}").asBoolean().ifNotExist().create()')
    
    def __GenerateVlabel(self, Vlabel_num):
        self.Vlabel_num = Vlabel_num
        for index in range(1, Vlabel_num + 1):
            label_name = f"Vlabel{index}"
            self.label2Vertex[label_name] = []
            self.Vlabelset.add(label_name)
            num = random.randint(1, self.property_num)
            properties = random.sample(self.property_set, num)
            self.Vlabel2prop[label_name] = properties

            if self.GDB_header != "hugegraph.traversal().": continue
            #only for hugegraph

            P = 'hugegraph.schema().vertexLabel(' + '"' + label_name + '"' + ').useAutomaticId().properties('
            for prop in properties:
                P = P + '"' + prop + '", '
            P = P + '"Id").create()'
            self.__output_statement(P)

    def __GenerateElabel(self, Elabel_num):
        self.Elabel_num = Elabel_num
        for index in range(1, Elabel_num + 1):
            label_name = f"Elabel{index}"
            self.Elabelset.add(label_name)
            num = random.randint(1, self.property_num)
            properties = random.sample(self.property_set, num)
            self.Elabel2prop[label_name] = properties
            self.Elabel2ST[label_name] = [list(random.sample(self.Vlabelset, 1))[0], list(random.sample(self.Vlabelset, 1))[0]]
            
            if self.GDB_header != "hugegraph.traversal().": continue
            #only for hugegraph

            P = "hugegraph.schema().edgeLabel(" + '"' + label_name + '"' + ").sourceLabel(" + '"' + self.Elabel2ST[label_name][0] + '"' + \
            ").targetLabel(" + '"' + self.Elabel2ST[label_name][1] + '"' +").properties("
            for prop in properties:
                P = P + '"' + prop + '", '
            P = P + '"Id").create()'
            self.__output_statement(P)

    def __GenerateVertex(self, vertex_num):
        for i in range(1, vertex_num + 1):
            dict = {}
            if i <= self.Vlabel_num: label_name = f"Vlabel{i}"
            else: label_name = list(random.sample(self.Vlabelset, 1))[0]
            self.Vertex2Label[i] = label_name
            self.label2Vertex[label_name].append(i)
            properties = self.Vlabel2prop[label_name]
            for prop in properties:
                value = self.Constants.Generate(self.Type[prop])
                dict[prop] = value
            dict["Id"] = (i, str(i))
            P = self.GDB_header + "addV(" + '"' + label_name + '"' + ")"
            self.Vertex2Prop[i] = dict

            for prop in dict.keys():
                P = P + ".property(" + '"' + prop + '", ' + dict[prop][1] + ")"
            self.__output_statement(P)

    def __GenerateEdge(self, edge_num):
        for i in range(1, edge_num + 1):
            label_name = list(random.sample(self.Elabelset, 1))[0]
            self.Edge2Label[i] = label_name
            properties = self.Elabel2prop[label_name]
            dict = {}
            for prop in properties:
                value = self.Constants.Generate(self.Type[prop])
                dict[prop] = value

            dict["Id"] = (i, str(i))
            self.Edge2Prop[i] = dict
            S, T = self.Elabel2ST[label_name][0], self.Elabel2ST[label_name][1]
            self.Edge2Ends[i] = [list(random.sample(self.label2Vertex[S], 1))[0], list(random.sample(self.label2Vertex[T], 1))[0]]
            P = self.GDB_header + "addE(" + '"' + label_name + '"' + \
            ').from(__.V().where(__.values("Id").is(eq(' + str(self.Edge2Ends[i][0]) \
            + ')))).to(__.V().where(__.values("Id").is(eq(' + str(self.Edge2Ends[i][1]) + "))))"

            for prop in dict.keys():
                P = P + ".property(" + '"' + prop + '", ' + dict[prop][1] + ")"
            self.__output_statement(P)

    def Graph_Generate(self, vertex_num = 30, edge_num = 150, Vlabel_num = 5, Elabel_num = 10, property_num = 30):
        # self.logger.info("Generating Gremlin Schema ...")
        self.__GenerateProp(property_num)
        self.__GenerateVlabel(Vlabel_num)
        self.__GenerateElabel(Elabel_num)
        self.__GenerateVertex(vertex_num)
        self.__GenerateEdge(edge_num)
        # self.logger.info("Gremlin Schema Generated !")

# if __name__ == "__main__":
#     G = GraphSchema()
#     print("OK")