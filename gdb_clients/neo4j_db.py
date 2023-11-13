from gdb_clients import GdbFactory
from neo4j import GraphDatabase, basic_auth
from typing import List
from configs.conf import *

class Neo4j(GdbFactory):
    def __init__(self, uri, username, passwd, database="neo4j"):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, passwd))
        self.session = self.driver.session()

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")

    def run(self, query: str):
        result = self.session.run(query)
        di = result.data()

        res = result.consume()
        t1 = res.result_available_after
        t2 = res.result_consumed_after
        return di, t1

    def get_execution_plan(self, query: str):
        result = self.session.run(query)
        result = result.consume()
        return result.plan

    def batch_run(self, queries: List[str]):
        self.clear()
        for stmt in queries:
            try:
                self.session.run(stmt)
            except Exception as e:
                print("create session error, ", e)


if __name__ == "__main__":
    neo4j = Neo4j(uri="bolt://localhost:10200", username=config.get('neo4j', 'username'), passwd=config.get('neo4j', 'passwd'))
    neo4j.clear()
