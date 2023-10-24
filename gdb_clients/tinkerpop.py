from gdb_clients import GdbFactory
from configs import config
import subprocess
# from .wrapper.tinkergraph_client import TinkerGraphClient
from gdb_clients.wrapper.tinkergraph_client import TinkerGraphClient
from gdb_clients.wrapper.cypher2gremlin import cypher2gremlin
import re

class Tinkerpop(GdbFactory):
    def __init__(self):
        self.client = TinkerGraphClient("localhost", "8182")
        self.clear()

    def run(self, query):
        if config.get('tinkerpop', 'input_mode') == "cypher":
            query = cypher2gremlin(query)
            ret = self.client.send_gremlin(query)
            return [i['@value'] for i in ret['result']['data']['@value'] if i], 0
        elif config.get('tinkerpop', 'input_mode') == "gremlin":
            ret = self.client.send_gremlin(query)
            return [i['@value'] for i in ret['result']['data']['@value'] if i], 0
        
    def batch_run(self, query):
        for q in query:
            self.run(q)

    def clear(self):
        self.client.delete_all_graphs()


if __name__ == "__main__":
    client = Tinkerpop()
    result, query_time = client.run(
        "MATCH (n0 :L6), (n1 :L3) WHERE true UNWIND [-1759295320, -1759295320] AS a0 UNWIND [(n1.k24), -1637829610] AS a1 OPTIONAL MATCH (n2 :L2)<-[r0 :T5]-(n3 :L0) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0), (n0 :L6) WHERE ((r0.k77) OR (n0.k39)) WITH (n0.k37) AS a2, a1, r0 OPTIONAL MATCH (n0) OPTIONAL MATCH (n0) RETURN (r0.k75) AS a3, (r0.k76) AS a4")
    print(len(result), query_time)
