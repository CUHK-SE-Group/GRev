from neo4j import GraphDatabase, basic_auth
from abc import ABC, abstractmethod


class GdbFactory(ABC):
    @abstractmethod
    def run(self, query):
        pass


class Neo4j(GdbFactory):
    def __init__(self, uri, username, passwd):
        self.driver = GraphDatabase.driver(uri, auth=basic_auth(username, passwd))
        self.session = self.driver.session()

    def run(self, query):
        self.session.run(query)

    def __del__(self):
        self.session.close()
        self.driver.close()


