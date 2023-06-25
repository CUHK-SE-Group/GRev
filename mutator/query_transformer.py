import random
from mutator.pattern_transformer import PatternTransformer


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
        # 随机选择一部分子句进行变异
        patterns = random.sample(patterns, random.randint(1, len(patterns)))
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
            asg = P.pattern2asg(pattern)
            new_pattern = P.asg2pattern(asg)
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
    print(Q.mutant_query_generator(
        "MATCH (n1 :L3)<-[r1 :T1]-(n2 :L4), (n3 :L0 :L1 :L4)<-[r2 :T2]-(n4 :L1 :L0)<-[r3 :T5]-(n5 :L3)"))
