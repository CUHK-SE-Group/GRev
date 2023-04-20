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

    def run(self, query):
        return self.session.run(query)

    def __del__(self):
        self.session.close()
        self.driver.close()


if __name__ == "__main__":
    client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
    with open("query_file/create.log", 'r') as f:
        query = f.readline()
        while query != '':
            query.replace('\n', '')
            try:
                result = client.run(query)
                print(len(list(result)))
            except Neo4jError as e:
                logging.error("An error occurred: ", e)
            query = f.readline()
