import time
import logging

from neo4j import GraphDatabase, basic_auth
from abc import ABC, abstractmethod

from neo4j.exceptions import Neo4jError, DatabaseError

from configs import logger
from utils.decorator import timeout_decorator, timeout_decorator2


class GdbFactory(ABC):
    @abstractmethod
    def run(self, query):
        pass


class Neo4j:
    def __init__(self, uri, username, passwd, database):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, passwd))

        # 获取所有数据库的名称
        with self.driver.session() as session:
            result = session.run("SHOW DATABASES")
            database_names = [record['name'] for record in result]

        # 检查指定的数据库是否在数据库名称列表中
        if database in database_names:
            print("The database exists.")
        else:
            session.run(f"CREATE DATABASE {self.database}")
        self.session = self.driver.session(database=database)

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")
        print("Clear Graph Schema.")

    def run(self, query):
        result = self.session.run(query, time_out=3)
        di = result.data()

        res = result.consume()
        t1 = res.result_available_after
        t2 = res.result_consumed_after
        return di, t1

    def create_graph(self, queries: []):
        self.clear()
        for stmt in queries:
            try:
                self.session.run(stmt)
            except Exception as e:
                logger.error("create session error, ", e)
        print("Graph schema Created.")

    def __del__(self):
        self.session.close()
        self.driver.close()


if __name__ == "__main__":
    client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
    result, query_time = client.run(
        "MATCH (n0 :L6), (n1 :L3) WHERE true UNWIND [-1759295320, -1759295320] AS a0 UNWIND [(n1.k24), -1637829610] AS a1 OPTIONAL MATCH (n2 :L2)<-[r0 :T5]-(n3 :L0) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0), (n0 :L6) WHERE ((r0.k77) OR (n0.k39)) WITH (n0.k37) AS a2, a1, r0 OPTIONAL MATCH (n0) OPTIONAL MATCH (n0) RETURN (r0.k75) AS a3, (r0.k76) AS a4")
    print(len(result), query_time)
    # client.create_graph("/Users/lincyaw/PycharmProjects/pattern-transformer/query_file/create.log")
    # with open("/Users/lincyaw/PycharmProjects/pattern-transformer/query_file/query.log", 'r') as f:
    #     query = f.readline()
    #     while query != '':
    #         query.replace('\n', '')
    #         try:
    #             result, query_time = client.run(query)
    #         except Neo4jError as e:
    #             logging.error("An error occurred: ", e)
    #         query = f.readline()
