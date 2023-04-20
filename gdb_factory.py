import time
import logging

from neo4j import GraphDatabase, basic_auth
from abc import ABC, abstractmethod

from neo4j.exceptions import Neo4jError


class GdbFactory(ABC):
    @abstractmethod
    def run(self, query):
        pass


class Neo4j:
    def __init__(self, uri, username, passwd):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, passwd))
        self.session = self.driver.session()
    
    def clear(self):
        self.session.run("MATCH (n) DETACH DELETE n")
        print("Clear Graph Schema.")


    def run(self, query):
        start_time = time.time()
        result = self.session.run(query)
        end_time = time.time()
        return result, end_time - start_time
    
    def create_graph(self, file_path):
        self.clear()
        with open(file_path, "r") as f:
            query = f.readline()
            while query != '': 
                query.replace('\n', '')
                try:
                    result = self.session.run(query)
                except Neo4jError as e:
                    logging.error("An error occurred: ", e)
                query = f.readline()
        print("Graph schema Created.")


    def __del__(self):
        self.session.close()
        self.driver.close()



if __name__ == "__main__":
    client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
    result, query_time = client.run("MATCH (n0 :L0 :L2 :L6)-[r0 :T1]->(n1 :L5), (n3 :L6) WHERE ((r0.id) > -1) OPTIONAL MATCH (n0 :L0)-[]->(n1 :L5)<-[]-(n2), (n3 :L6) WHERE ((n1.k33) OR (n0.k4)) OPTIONAL MATCH (n3 :L6), (n1 :L5)<-[]-(n0), (n1 :L5)<-[]-(n2 :L5)WITH DISTINCT max('S') AS a0, r0, (r0.k51) AS a1 WHERE (-1577216923 = -1577216923) RETURN a1, (r0.k51) AS a2")
    client.create_graph("query_file/create.log")
    with open("query_file/query.log", 'r') as f:
        query = f.readline()
        while query != '':
            query.replace('\n', '')
            try:
                result, query_time = client.run(query)
            except Neo4jError as e:
                logging.error("An error occurred: ", e)
            query = f.readline()
