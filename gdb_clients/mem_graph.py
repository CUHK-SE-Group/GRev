from gqlalchemy import Memgraph
from gdb_clients import GdbFactory
from configs.conf import  config


class MemGraph(GdbFactory):
    def __init__(self):
        self.connection = Memgraph(host="memgraph", port=7687)

    def run(self, query):
        res = self.connection.execute_and_fetch(query)
        return list(res), 0

    def batch_run(self, query):
        for q in query:
            self.connection.execute(q)

    def clear(self):
        self.connection.execute("MATCH (n) DETACH DELETE n")

