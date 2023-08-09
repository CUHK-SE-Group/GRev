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
    tails = [".dedup().count()", ".count()"]
    for i in range(0, query_num):
        tail = random.choice(tails)
        Pattern.GenPatterns()
        q1 = GDB_header + "V()" + Pattern.to_string() + tail
        asg = Pattern.to_asg()
        q2 = GDB_header + "V()" + asg.to_string() + tail
        res.append({"Query1" : q1, "Query2" : q2})

    with open(queryfile, "w", encoding="utf+8") as f:
        json.dump(res, f)


def GenTestcase_without_match(createfile, queryfile, query_num, GDB_header = "g."):
    G = GraphSchema(GDB_header = GDB_header, output_file = createfile)
    G.Graph_Generate()
    PG = PatternGenerator(G)
    Pattern = GraphPattern(PG)

    res = []
    tails = [".dedup().count()", ".count()"]
    for i in range(0, query_num):
        tail = random.choice(tails)
        Pattern.GenPatterns()
        q1 = GDB_header + "V()" + Pattern.to_string_without_match() + tail
        asg = Pattern.to_asg()
        q2 = GDB_header + "V()" + asg.to_string_without_match() + tail
        res.append({"Query1" : q1, "Query2" : q2})

    with open(queryfile, "w", encoding="utf+8") as f:
        json.dump(res, f)

if __name__ == "__main__":
    for i in range(1000):
        GenTestcase_without_match(f"./query_producer/gremlin_generator/create-{i}.log", f"./query_producer/gremlin_generator/query-{i}.log", 2000)