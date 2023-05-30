import redis
from redisgraph import Graph

from gdb_clients import GdbFactory


class Redis(GdbFactory):
    def __init__(self, uri, database):
        self.redis_con = redis.Redis(host=uri, port=6379)
        self.graph = Graph(database, self.redis_con)

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")

    def run(self, query):
        query = query.replace(';', '')
        result = self.graph.query(query)
        print(result.header)
        return result.result_set, result.run_time_ms

    def batch_run(self, queries):
        for i in queries:
            i = i.replace(';', '')
            self.run(i)
        return


if __name__ == "__main__":
    r = Redis("10.20.10.27", "test_graph")

    q = "MATCH (n0 :L4 :L0 :L3), (n0 :L4 :L0 :L3)<-[r0 :T5]-(n1 :L1 :L2), (n2)<-[r1 :T3]-(n1 :L1 :L2), (n4 :L2 :L0)-[r3 :T5]->(n5 :L1 :L4 :L3) WHERE (((((r1.k53) <> (n0.k27)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r1.id) <> (r3.id))) OPTIONAL MATCH (n1), (n1)-[]->(n0), (n8), (n7 :L4)<-[r5 :T5]-(n8), (n1)-[]->(n2), (n7 :L4), (n6 :L2), (n6 :L2)-[r4 :T2]->(n7 :L4) WHERE (((r4.id) > -1) AND ((r4.id) <> (r5.id))) OPTIONAL MATCH (n7)<-[r6 :T4]-(n5 :L3), (n9 :L4), (n9 :L4)-[r7 :T2]->(n5 :L3) WHERE (((r6.id) > -1) AND ((r6.id) <> (r7.id))) RETURN (n5.k21) AS a0, (n0.k24) AS a1, (n9.k25) AS a2, (r6.k58) AS a3 ORDER BY a3"
    re, t = r.run(q)
    print(re, t)