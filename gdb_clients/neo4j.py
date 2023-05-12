from gdb_clients import GdbFactory
from configs import logger
from neo4j import GraphDatabase, basic_auth


class Neo4j(GdbFactory):
    def __init__(self, uri, username, passwd, database):
        self.database = database
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, passwd))
        self.session = self.driver.session(database=database)

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")

    def run(self, query):
        result = self.session.run(query)
        di = result.data()

        res = result.consume()
        t1 = res.result_available_after
        t2 = res.result_consumed_after
        return di, t1

    def batch_run(self, queries: []):
        self.clear()
        for stmt in queries:
            try:
                self.session.run(stmt)
            except Exception as e:
                logger.error("create session error, ", e)



if __name__ == "__main__":
    client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
    result, query_time = client.run(
        "MATCH (n0 :L6), (n1 :L3) WHERE true UNWIND [-1759295320, -1759295320] AS a0 UNWIND [(n1.k24), -1637829610] AS a1 OPTIONAL MATCH (n2 :L2)<-[r0 :T5]-(n3 :L0) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0), (n0 :L6) WHERE ((r0.k77) OR (n0.k39)) WITH (n0.k37) AS a2, a1, r0 OPTIONAL MATCH (n0) OPTIONAL MATCH (n0) RETURN (r0.k75) AS a3, (r0.k76) AS a4")
    print(len(result), query_time)
