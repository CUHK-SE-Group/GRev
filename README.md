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

## 运行测试
在根目录运行测试，如测试Neo4j 使用 ```python ./database_test/neo4j/TestNeo4j.py```
如果是命令行执行需要 ```export PYTHONPATH=./:$PYTHONPATH```

### Detected Bugs:
[Neo4j-13168](https://github.com/neo4j/neo4j/issues/13168)
