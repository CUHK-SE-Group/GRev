# pattern-transformer


## 目录结构说明

```
configs: 配置全局使用的一些配置文件和公用函数
database_tests: 针对不同的db实现的测试逻辑
gdb_client: 针对不同db实现的客户端连接，用于与db服务端通信交互
logs: 日志文件
mutator: 突变的主要逻辑
query_file: 用于测试的原始query请求的集合
```

## 核心算法验证

最核心的MR关系的变换算法位于 `mutator/pattern_transformer.py` 中。 

如何验证该算法：
1. 在`mutator/test_cases.ini`里添加pattern作为测试用例。
2. 在当前目录运行pytest，单元测试会读取文件里的测试用例进行测试

### Sample input for new pattern mutator:
```cypher
(n2:(L7&L2&!L3))-[r32:((T1&T7)|(%)) WHERE (r32.p19 <> r24.p2) OR (NOT (r32.p2 = r6.p6))]->(n11:(!L1&(L0)))<-[r33:(!%&!!!(T3)|!!T5)]-(n20:(L4)), (n6:(!!L6&%&(L1)))<-[r34:(!T0|T0|!!T1|!%) {p19: "1EGGYIgd7PMxHW"}]-(n5:((L5)|!(L2)) {p15: false})-[r35:((T1)|!!T0|!(T6))]-(n4:(!!%&!!!!!(%&(L2))))-[:(!T6) *]-(n6:(!!L7&%|!!L2&!!(%)))<-[:(!!!T3&T6) *]-(n9:((L5)|L6|!!L5|!!(L1))), (n21:((!L2|!L3&(L0|L5)))), (n10)-[r36:(T3&%)]-(n3:(L5&L1&L5) {p10: "T"})
```

## 运行测试
在根目录运行测试，如测试Neo4j 使用 ```python ./database_test/neo4j/TestNeo4j.py```
如果是命令行执行需要 ```export PYTHONPATH=./:$PYTHONPATH```

## Detected Bugs
[Neo4j-13168](https://github.com/neo4j/neo4j/issues/13168) Status: Duplicated (with [Neo4j-13085](https://github.com/neo4j/neo4j/issues/13085))

[Neo4j-13170](https://github.com/neo4j/neo4j/issues/13170) Status: Fixed

[Neo4j-13212](https://github.com/neo4j/neo4j/issues/13212) Status: Duplicated

[Neo4j-13225](https://github.com/neo4j/neo4j/issues/13225) Status: Confirmed/Intended

[Neo4j-13229](https://github.com/neo4j/neo4j/issues/13229) Status: Confirmed

[Neo4j-13233](https://github.com/neo4j/neo4j/issues/13233) Status: Intended

[Neo4j-13234](https://github.com/neo4j/neo4j/issues/13234) Status: Intended

[Neo4j-13235](https://github.com/neo4j/neo4j/issues/13235) Status: Intended (Related to 3 bugs)

[Neo4j-13236](https://github.com/neo4j/neo4j/issues/13236) Status: Intended

[Memgraph-948](https://github.com/memgraph/memgraph/issues/948) Status: Confirmed (Related to 2 bugs)

[Memgraph-954](https://github.com/memgraph/memgraph/issues/954) Status: Intended

[RedisGraph-3081](https://github.com/RedisGraph/RedisGraph/issues/3081) Status: Intended

[RedisGraph-3091](https://github.com/RedisGraph/RedisGraph/issues/3091) Status: Intended

[RedisGraph-3093](https://github.com/RedisGraph/RedisGraph/issues/3093) Status: Intended

[RedisGraph-3100](https://github.com/RedisGraph/RedisGraph/issues/3100) Status: Intended

[RedisGraph-3114](https://github.com/RedisGraph/RedisGraph/issues/3114) Status: Intended

[TinkerPop-2961](https://issues.apache.org/jira/projects/TINKERPOP/issues/TINKERPOP-2961) Status: Confirmed





