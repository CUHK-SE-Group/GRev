from gdb_clients import GdbFactory
from configs import config
from .wrapper.hugegraph_gremlin_client_plus import HugeGraphClient
from gdb_clients.wrapper.cypher2gremlin import cypher2gremlin

class HugeGraph(GdbFactory):
    def __init__(self):
        self.client = HugeGraphClient("10.26.1.146", "7779")

    def run(self, query):
        query = cypher2gremlin(query)
        ret = self.client.send_gremlin(query)
        return [i['@value'] for i in ret['result']['data']['@value'] if i], 0
        
    def batch_run(self, query):
        for q in query:
            self.run(q)

    def clear(self):
        self.client.delete_all_graphs()
