# The main file that produce the query statements
import random
import copy
from cypher.memgraph.pattern_clause import PatternGenerator
from cypher.schema import GraphSchema
from mutator.redis.pattern_mutator import PatternMutator

class QueryGenerator:
    def __init__(self, output_file="./cypher/memgraph/schema/create.log"):
        self.G = GraphSchema()
        self.G.gen(output_file = output_file)
        self.pattern_generator = None
        self.pattern_mutator = PatternMutator()
        self.generated_match = None
        self.generated_optional_match = None

    def gen_match(self):
        if self.generated_optional_match or (self.generated_match and random.randint(1, 3) > 1):
            res = "OPTIONAL MATCH "
            self.generated_optional_match = True
        else:
            res = "MATCH "
            self.generated_match = True

        pattern1 = self.pattern_generator.gen_pattern()
        pattern2 = self.pattern_mutator.gen_pattern(pattern1)

        return res + pattern1, res + pattern2
    
    def gen_where_predicate(self):
        res = "WHERE "
        predicate = self.pattern_generator.where_generator.gen_exp()
        return res + predicate, res + predicate
    
    def gen_where_exists_pattern(self):
        res = "WHERE exists("
        pattern1 = self.pattern_generator.gen_path(no_new_variables = True, only_path=True)
        pattern2 = self.pattern_mutator.rev_pattern(pattern1)
        return res + pattern1 + ")", res + pattern2 + ")"
    
    def gen_return(self):
        return "RETURN *", "RETURN *"

    def gen_query(self):        
        self.pattern_generator = PatternGenerator(self.G)

        self.generated_match = self.generated_optional_match = False

        query1, query2, last_funcs = "", "", None
        num = random.randint(1, 5)
        for _ in range(0, num):
            if last_funcs != self.gen_match:
                clause1, clause2 = self.gen_match()
                query1 += clause1 + " "
                query2 += clause2 + " "
                last_funcs = self.gen_match
            else:
                funcs = [self.gen_match, self.gen_where_predicate,
                         self.gen_where_exists_pattern]
                random_funcs = random.choice(funcs)
                clause1, clause2 = random_funcs()
                query1 += clause1 + " "
                query2 += clause2 + " "
                last_funcs = random_funcs

        clause1, clause2 = self.gen_return()
        return query1 + clause1, query2 + clause2

if __name__ == "__main__":
    query_generator = QueryGenerator()
    with open("./cypher/memgraph/query_sample.in", mode="w+") as f:
        for _ in range(1000):
            print(query_generator.gen_query()[random.randint(0, 1)], file=f)
