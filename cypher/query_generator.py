# The main file that produce the query statements
import random
import copy
import re
from cypher.pattern_clause import PatternGenerator
from cypher.schema import GraphSchema
from mutator.refactored.pattern_mutator import PatternMutator

class QueryGenerator:
    def __init__(self, output_file="./cypher/schema/create.log"):
        self.G = GraphSchema()
        self.G.gen(output_file = output_file)
        self.pattern_generator = None
        self.pattern_mutator = PatternMutator()

    def gen_match(self):
        if self.generated_match == True and random.randint(1, 3) > 1:
            res = "OPTIONAL MATCH "
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
    
    def gen_where_pattern(self):
        res = "WHERE "
        pattern1 = self.pattern_generator.gen_path(no_new_variables = True, only_path = True)
        pattern2 = self.pattern_mutator.rev_pattern(pattern1)
        return res + pattern1, res + pattern2
    
    def gen_where_exists_pattern(self):
        res = "WHERE EXISTS {"
        pattern1 = self.pattern_generator.gen_pattern(no_new_variables = True)
        pattern2 = self.pattern_mutator.gen_pattern(pattern1)
        return res + pattern1 + " }", res + pattern2 + " }"
    
    def gen_return(self):
        if random.randint(1, 2) == 1: return "RETURN *", "RETURN *"
        else:
            pattern1 = self.pattern_generator.gen_pattern()
            pattern2 = self.pattern_mutator.gen_pattern(pattern1)
            res = "RETURN COUNT { "
            return res + pattern1 + " } AS a1", res + pattern2 + " } AS a1" 
    
    def gen_query(self):        
        self.pattern_generator = PatternGenerator(self.G)
        self.generated_match = False

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
                        self.gen_where_exists_pattern, self.gen_where_pattern]
                random_funcs = random.choice(funcs)
                clause1, clause2 = random_funcs()
                query1 += clause1 + " "
                query2 += clause2 + " "
                last_funcs = random_funcs

        clause1, clause2 = self.gen_return()
        
        text = query1 + clause1
        matches = list(set(re.findall(r'n\d+', text)))
        for i in range(len(matches)//2):
            original = matches[i]
            # 获取要替换的字符串
            replacement = matches[-i - 1]
            
            # 替换原始文本中的匹配字符串
            text = text.replace(original, "TEMP_PLACEHOLDER" + str(i))  # 使用临时占位符
            text = text.replace(replacement, original)
            text = text.replace("TEMP_PLACEHOLDER" + str(i), replacement)
        if len(matches)>1:
            assert text != query1+clause1
        return query1+clause1, query2 + clause2

if __name__ == "__main__":
    query_generator = QueryGenerator()
    for _ in range(10):
        print(query_generator.gen_query())
    print("OK")