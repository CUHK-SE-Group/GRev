from config import logger
from gdb_factory import *
from query_transformer import *
from copy import deepcopy

from pandas import DataFrame
import pandas as pd


class Neo4jTester():
    def __compare(self, result1, result2):
        data1 = deepcopy(result1)
        data2 = deepcopy(result2)
        return not(data1 == data2)

    def Testing(self, create_file, query_file):
        client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
        client.create_graph(create_file)
        Q = QueryTransformer()
        with open(query_file, 'r') as f:
            query = f.readline()
            query_counter = 0
            while query != '':
                query = query.replace('\n', '')
                query_counter += 1
                print(query_counter, query)
                try:
                    result, query_time1 = client.run(query)
                    result1 = result.data()
                except Neo4jError as e:
                    logger.info("Unexpected exception: ", e)
                    logger.info("Triggering Query: " + query)
                    query = f.readline()
                    continue

                for step in range(0, 5):
                    new_query = Q.mutant_query_generator(query)
                    # if new_query == query: continue
                    
                    try:
                        result, query_time2 = client.run(new_query)
                        result2 = result.data()
                    except Neo4jError as e:
                        logger.info("Unexpected exception: ", e)
                        logger.info("Triggering Query: " + new_query)
                        continue

                    if self.__compare(result1, result2):
                        logger.info("Logic inconsistency: ")
                        logger.info("Query1 " + query)
                        logger.info("Query2 " + new_query)

                    elif query_time1 > 1 and query_time2 > 1 and\
                    (query_time1 > 2 * query_time2 or query_time1 < 0.5 * query_time2):
                        logger.info("Performance inconsistency: ")
                        logger.info("Query1 " + query)
                        logger.info(f"Query Time1 {query_time1}")
                        logger.info("Query2 " + new_query)
                        logger.info(f"Query Time2 {query_time2}")
                
                query = f.readline()

if __name__ == "__main__":
    Tester = Neo4jTester()
    Tester.Testing("query_file/create.log", "query_file/query.log")