# The main file that produce the query statements
import random
from cypher.pattern_clause import PatternGenerator
from cypher.schema import GraphSchema

class QueryGenerator:
    def __init__(self, G : GraphSchema):
        self.pattern_generator = PatternGenerator(self.G)



if __name__ == "__main__":
    pass