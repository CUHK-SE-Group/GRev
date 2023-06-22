from gqlalchemy import Memgraph
from gdb_clients import GdbFactory
from configs.conf import  config
import time


class MemGraph(GdbFactory):
    def __init__(self):
        self.connection = Memgraph(host=config.get("memgraph", "uri"), port=7687)

    def run(self, query):
        start_time = time.time()
        res = self.connection.execute_and_fetch(query)
        execution_time = time.time() - start_time
        return list(res), execution_time*100000

    def batch_run(self, query):
        for q in query:
            self.connection.execute(q)

    def clear(self):
        self.connection.execute("MATCH (n) DETACH DELETE n")

