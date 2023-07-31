from mutator.redis.pattern_transformer import PatternTransformer


class QueryTransformer():
    # 解析查询字符串，提取出 "MATCH " 子句的位置
    def __parse_patterns(self, query):
        # 查询字符串中 "MATCH " 的起始位置
        pos = query.find("MATCH ")
        # 用于查询的关键字列表
        keywords = ["RETURN ", "OPTIONAL MATCH ", "WHERE ", "CONTAINS ", "WITHIN ",
                    "WITH ", "UNION ", "ALL ", "UNWIND ", "AS ", "MERGE ", "ON ",
                    "CREATE ", "SET ", "DETACH ", "DELETE ", "REMOVE ", "CALL ",
                    "YIELD ", "DISTINCT ", "ORDER ", "BY ", "L_SKIP ", "LIMIT ",
                    "ASCENDING ", "ASC ", "DESCENDING ", "DESC ", "OR ", "XOR ",
                    "AND ", "NOT ", "STARTS ", "ENDS ", "CONTAINS ", "IN ", "IS ",
                    "NULL ", "COUNT ", "CASE ", "ELSE ", "END ", "WHEN ", "THEN ",
                    "ANY ", "NONE ", "SINGLE ", "EXISTS ", "MATCH "
                    ]
        # 用于保存 "MATCH " 子句位置的列表
        res = []
        while pos != -1:
            # 计算下一个关键字的位置
            f = lambda x: query.find(x, pos + 1) if query.find(x, pos + 1) > -1 else len(query)
            next_pos = min(f(x) for x in keywords)
            # 将 "MATCH " 子句的位置添加到结果列表
            res.append((pos + len("MATCH "), next_pos))
            pos = query.find("MATCH ", pos + 1)

        return res

    # 变异查询字符串
    def mutant_query_generator(self, query):
        # 获取查询字符串中的 "MATCH " 子句
        patterns = self.__parse_patterns(query)
        # 全部变异
        new_query = ""
        index = 0
        # 对选择的子句进行变异
        for pos in sorted(patterns):
            while index < pos[0]:
                new_query = new_query + query[index]
                index = index + 1
            pattern = query[pos[0]:pos[1]]
            # 使用 PatternTransformer 进行变异
            P = PatternTransformer()
            asg = P.pattern_to_asg(pattern)
            new_pattern = P.asg_to_pattern(asg)
            new_asg = P.pattern_to_asg(new_pattern)
            assert asg.get_comparable() == new_asg.get_comparable()
            new_query = new_query + new_pattern + " "
            index = pos[1]
        # 添加剩余部分到新查询字符串
        while index < len(query):
            new_query = new_query + query[index]
            index = index + 1
        return new_query


# 测试代码
if __name__ == "__main__":
    Q = QueryTransformer()
    print(Q.mutant_query_generator('query = MATCH (n0 {id : 10}), (n1 {id : 78}) MERGE(n0)-[r :T4{k60 : "Z", k62 : true, k61 : 474288688, k64 : 1763262399, k63 : -1849292085, k66 : true, id : 293}]->(n1);'))
