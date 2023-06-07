import age
from age.gen.AgtypeParser import *
from age.models import Vertex
from gdb_clients import GdbFactory
from configs import config
import re

def add_space_before_colon(text):
    words = text.split(":")
    modified_text = " :".join(words)
    return modified_text

class AgeDB(GdbFactory):
    def __init__(self):
        graph=config.get('age', 'graph_name')
        host=config.get('age', 'host')
        port=config.get('age', 'port')
        dbname=config.get('age', 'dbname')
        user=config.get('age', 'user')
        password=config.get('age', 'password')
        self.ag = age.connect(graph=graph, host=host, port=port, dbname=dbname, user=user, password=password)
        self.ag.setGraph(config.get('age', 'graph_name'))

    def run(self, query):
        pattern = r':L\d+'
        query = re.sub(pattern, '', query)
        query = query.replace(";", "")
        cursor = self.ag.execCypher(query)
        for row in cursor:
            print("Vertex: %s , Type: %s " % (Vertex, type(row[0])))
        return [s], 0

    def batch_run(self, query):
        for q in query:
            string = q
            pattern = r':L\d+'
            q = re.sub(pattern, '', string)
            q = q.replace(";", "")
            self.ag.execCypher(q)

    def clear(self):
        self.ag.execCypher("MATCH (n) DETACH DELETE n")



if __name__ == "__main__":
    client = AgeDB()
    result, query_time = client.run(
        "MATCH (n0 :L6), (n1 :L3) WHERE true UNWIND [-1759295320, -1759295320] AS a0 UNWIND [(n1.k24), -1637829610] AS a1 OPTIONAL MATCH (n2 :L2)<-[r0 :T5]-(n3 :L0) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0), (n0 :L6) WHERE ((r0.k77) OR (n0.k39)) WITH (n0.k37) AS a2, a1, r0 OPTIONAL MATCH (n0) OPTIONAL MATCH (n0) RETURN (r0.k75) AS a3, (r0.k76) AS a4")
    print(len(result), query_time)
