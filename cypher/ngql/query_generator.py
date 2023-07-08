# The main file that produce the query statements
import random
from cypher.ngql.pattern_clause import PatternGenerator
from cypher.ngql.schema import GraphSchema
from mutator.ngql.pattern_mutator import PatternMutator

class QueryGenerator:
    def __init__(self, output_file="./ngql/schema/create.log", num_vertices=15, num_edges=100, num_props=15,
                 num_vertex_tags=6, num_edge_tags=6):
        self.G = GraphSchema()
        self.G.gen(output_file = output_file, num_vertices=num_vertices, num_edges=num_edges,
                   num_props=num_props, num_vertex_tags=num_vertex_tags, num_edge_tags=num_edge_tags)
        self.pattern_mutator = PatternMutator()
        self.last_one_is_optional = None

    def gen_match(self):
        if self.generated_match == True and random.randint(1, 3) > 1:
            res = "OPTIONAL MATCH "
            self.last_one_is_optional = True
        else:
            res = "MATCH "
            self.generated_match = True
            self.last_one_is_optional = False
        
        pattern1 = self.pattern_generator.gen_pattern()
        pattern2 = self.pattern_mutator.gen_pattern(pattern1)

        return res + pattern1, res + pattern2

    def gen_where_predicate(self):
        res = "WHERE "
        predicate = self.pattern_generator.where_generator.gen_exp()
        return res + predicate, res + predicate
    
    def gen_where_pattern(self):
        res = "WHERE "
        pattern1 = self.pattern_generator.gen_path(no_new_variables = True, num_lo=2)
        pattern2 = self.pattern_mutator.rev_pattern(pattern1)
        return res + pattern1, res + pattern2
    
    def gen_where_exists_pattern(self):
        res = "WHERE EXISTS {"
        pattern1 = self.pattern_generator.gen_pattern(no_new_variables = True)
        pattern2 = self.pattern_mutator.gen_pattern(pattern1)
        return res + pattern1 + " }", res + pattern2 + " }"
    
    def gen_return(self):
        # Nebula Graph does not seem to support COUNT stuff :)
        if random.randint(1, 1) == 1: return "RETURN *", "RETURN *"
        else:
            pattern1 = self.pattern_generator.gen_pattern()
            pattern2 = self.pattern_mutator.gen_pattern(pattern1)
            res = "RETURN COUNT { "
            return res + pattern1 + " } AS a1", res + pattern2 + " } AS a1" 
    
    def gen_query(self):        
        self.pattern_generator = PatternGenerator(self.G)
        self.generated_match = False

        query1, query2, last_funcs = "", "", None
        num = random.randint(1, 2)
        for _ in range(0, num):
            if last_funcs != self.gen_match:
                clause1, clause2 = self.gen_match()
                query1 += clause1 + " "
                query2 += clause2 + " "
                last_funcs = self.gen_match
            else:
                if not self.last_one_is_optional:
                    funcs = [self.gen_match, self.gen_where_predicate, self.gen_where_pattern]
                    random_funcs = random.choice(funcs)
                else:
                    random_funcs = self.gen_match
                clause1, clause2 = random_funcs()
                query1 += clause1 + " "
                query2 += clause2 + " "
                last_funcs = random_funcs

        clause1, clause2 = self.gen_return()
        return query1 + clause1, query2 + clause2

if __name__ == "__main__":
    qg = QueryGenerator(num_vertices=3, num_edges=3, num_props=8, num_vertex_tags=2, num_edge_tags=2)
    with open('./ngql/query_sample.in', 'w+') as f:
        for _ in range(100):
            print(qg.gen_query()[0], file=f)
