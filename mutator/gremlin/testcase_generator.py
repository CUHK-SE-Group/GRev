import json
import random
from mutator.gremlin.schema import GraphSchema
from mutator.gremlin.asg import ASG
from mutator.gremlin.generator import PatternGenerator
from mutator.gremlin.patterns import GraphPattern

def GenTestcase(createfile, queryfile, query_num, GDB_header = "g."):
    G = GraphSchema(GDB_header = GDB_header, output_file = createfile)
    G.Graph_Generate()
    PG = PatternGenerator(G)
    Pattern = GraphPattern(PG)

    res = []
    for i in range(0, query_num):
        Pattern.GenPatterns()
        q1 = GDB_header + "V()" + Pattern.to_string() + ".count()"
        asg = Pattern.to_asg()
        q2 = GDB_header + "V()" + asg.to_string() + ".count()"
        res.append({"Query1" : q1, "Query2" : q2})

    with open(queryfile, "w", encoding="utf+8") as f:
        json.dump(res, f)

if __name__ == "__main__":
    GenTestcase("./mutator/gremlin/schemas/create-01.log", "./mutator/gremlin/schemas/query-01.json", 1000)