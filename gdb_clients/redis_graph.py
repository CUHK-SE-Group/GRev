import redis
from redisgraph import Graph

from gdb_clients import GdbFactory


class Redis(GdbFactory):
    def __init__(self, uri, database, reset=True):
        self.redis_con = redis.Redis(host=uri, port=6379, socket_timeout=10)
        self.graph = Graph(database, self.redis_con)
        if reset:
            self.clear()

    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")

    def get_plan(self, query):
        """Returns tuple of execution plans"""
        query = query.replace(';', '')
        plan = self.redis_con.execute_command("GRAPH.EXPLAIN", self.graph.name, query)
        plan = [step.decode('utf-8') if isinstance(step, bytes) else step for step in plan]
        return tuple(plan)

    def run(self, query):
        query = query.replace(';', '')
        result = self.graph.query(query)
        return result.result_set, result.run_time_ms

    def batch_run(self, queries):
        for i in queries:
            i = i.replace(';', '')
            self.run(i)


if __name__ == "__main__":
    r = Redis("localhost", "validate", True)
    with open("query_file/redis.log") as f:
        cmd = f.readlines()
        try:
            r.batch_run(cmd)
        except Exception as e:
            print(e)
        

