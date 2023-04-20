def parse_patterns(query):
    #返回所有MATCH patterns的左闭右开区间
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
        # print(query[pos + len("MATCH "): next_pos])
        pos = query.find("MATCH ", pos + 1)
        
    return res

if __name__ == "__main__":
    parse_patterns("MATCH (n0 :L1 :L5)<-[r0 :T3]-(n1 :L3)-[r1 :T3]->(n2 :L1), (n2 :L5)<-[r2 :T4]-(n1) WHERE (((((r0.id) > -1) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r2.id))) AND ((r1.id) <> (r2.id))) UNWIND [(n1.k24)] AS a0 OPTIONAL MATCH (n2 :L1)<-[]-(n1 :L3) RETURN a0")