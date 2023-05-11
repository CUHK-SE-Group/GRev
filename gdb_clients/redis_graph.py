import redis
from redisgraph import Graph


class Redis:
    def __init__(self, uri, database):
        self.redis_con = redis.Redis(host=uri, port=6379)
        self.graph = Graph(database, self.redis_con)

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")
        print("Clear Graph Schema.")

    def run(self, query):
        query = query.replace(';', '')
        result = self.graph.query(query)
        return result.result_set

    def create_graph(self, queries):
        for i in queries:
            i = i.replace(';', '')
            self.run(i)
        return


if __name__ == "__main__":
    r = Redis("10.20.10.27", "test_graph")
    re = r.run("MATCH (n0)<-[r0 :T3]-(n1), (n2 :L2) WHERE ((r0.id) > -1) MATCH (n2) OPTIONAL MATCH (n3 :L0 :L3 :L5)-[r1 :T0]->(n1)-[r2 :T1]->(n0) WHERE (((r0.k55) <= (r2.k46)) AND ((r1.id) <> (r2.id))) OPTIONAL MATCH (n3)-[]->(n1)-[]->(n0) WHERE ((n2.k15) >= (n2.k15)) RETURN (r1.k43) AS a0, (r0.k57) AS a1, (r1.k40) AS a2, (r1.k43) AS a3")
    print(re)
