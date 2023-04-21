import concurrent.futures
import threading
from copy import deepcopy

from gdb_clients import *
from configs.config import logger
from mutator.query_transformer import QueryTransformer
from compare.hash_nested_dict import hash_dictionary


def compare(result1, result2):
    data1 = deepcopy(result1)
    data2 = deepcopy(result2)
    if len(data1) != len(data2): return 0 
    return not ( sorted([hash_dictionary(x) for x in data1]) \
        == sorted([hash_dictionary(x) for x in data2]) )


class Neo4jTester():
    def __init__(self):
        self.connections = {}

    def get_connection(self):
        thread_id = threading.get_ident()
        if thread_id not in self.connections:
            self.connections[thread_id] = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
        return self.connections[thread_id]

    def process_query(self, query: str, transformer: QueryTransformer):
        client = self.get_connection()
        query = query.replace('\n', '')
        try:
            result, query_time1 = client.run(query)
            result1 = result.data()
        except Neo4jError as e:
            logger.info(f"Neo4j exception: {e}. \n Triggering Query: {query}")
            return
        except Exception as e:
            logger.info(f"Unexpected exception: {e}. \n Triggering Query: {query}")
            return

        for step in range(0, 5):
            new_query = transformer.mutant_query_generator(query)
            try:
                result, query_time2 = client.run(new_query)
                result2 = result.data()
                if compare(result1, result2):
                    logger.warn(f"Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
                    break
                elif query_time1 > 1 and query_time2 > 1 and \
                        (query_time1 > 2 * query_time2 or query_time1 < 0.5 * query_time2):
                    logger.info(
                        f"Performance inconsistency. \n Query1: {query} \n using time: {query_time1} \n Query2: {new_query} \n using time: {query_time2}")
                    break
            except Neo4jError as e:
                logger.info(f"Neo4j exception: {e}. \n Triggering Query: {new_query}")
                break
            except Exception as e:
                logger.info(f"Unexpected exception: {e}. \n Triggering Query: {new_query}")
                break
                
    def Testing(self, create_file, query_file):
        client = Neo4j("bolt://10.20.10.27:7687", "neo4j", "testtest")
        client.create_graph(create_file)
        Q = QueryTransformer()
        with open(query_file, 'r') as f:
            queries = f.readlines()
            queries = [query.replace('\n', '') for query in queries]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.process_query, query, Q): query for query in queries}

            for future in concurrent.futures.as_completed(futures):
                query = futures[future]
                print(query)
                future.result()


if __name__ == "__main__":
    Tester = Neo4jTester()
    Tester.Testing("query_file/create.log", "query_file/query.log")
