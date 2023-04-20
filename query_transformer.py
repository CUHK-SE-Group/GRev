import random
from pattern_transformer import *

class QueryTransformer():
    def __parse_patterns(self, query):
        pos = query.find("MATCH ")
        keywords = ["RETURN ", "OPTIONAL MATCH ", "WHERE ", "CONTAINS ", "WITHIN ",
                    "WITH ", "UNION ", "ALL ", "UNWIND ", "AS ", "MERGE ", "ON ",
                    "CREATE ", "SET ", "DETACH ", "DELETE ", "REMOVE ", "CALL ",
                    "YIELD ", "DISTINCT ", "ORDER ", "BY ", "L_SKIP ", "LIMIT ",
                    "ASCENDING ", "ASC ", "DESCENDING ", "DESC ", "OR ", "XOR ",
                    "AND ", "NOT ", "STARTS ", "ENDS ", "CONTAINS ", "IN ", "IS ",
                    "NULL ", "COUNT ", "CASE ", "ELSE ", "END ", "WHEN ", "THEN ",
                    "ANY ", "NONE ", "SINGLE ", "EXISTS ", "MATCH "
        ]
        res = []
        while pos != -1:
            f = lambda x: query.find(x, pos + 1) if query.find(x, pos + 1) > -1 else len(query)
            next_pos = min(f(x) for x in keywords)
            res.append((pos + len("MATCH "), next_pos))
            pos = query.find("MATCH ", pos + 1)
            
        return res
    
    def mutant_query_generator(self, query):
        patterns = self.__parse_patterns(query)
        patterns = random.sample(patterns, random.randint(1, len(patterns)))
        new_query = ""
        index = 0
        for pos in sorted(patterns):
            while index < pos[0]: 
                new_query = new_query + query[index]
                index = index + 1
            pattern = query[pos[0]:pos[1]]
            P = PatternTransformer()
            asg = P.pattern2asg(pattern)
            new_pattern = P.asg2pattern(asg)
            new_query = new_query + new_pattern + " "
            index = pos[1]
        while index < len(query):
            new_query = new_query + query[index]
            index = index + 1
        return new_query

if __name__ == "__main__":
    Q = QueryTransformer()
    print(Q.mutant_query_generator("MATCH (n0 :L0 :L2 :L6)-[r0 :T1]->(n1 :L5), (n3 :L6) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0 :L0)-[]->(n1 :L5)<-[]-(n2), (n3 :L6) WHERE ((n1.k33) OR (n0.k4)) OPTIONAL MATCH (n0)-[]->(n1 :L5)<-[]-(n2 :L5), (n3 :L6), (n3) WITH DISTINCT max('S') AS a0, r0, (r0.k51) AS a1 WHERE (-1577216923 = -1577216923) RETURN a1, (r0.k51) AS a2"))