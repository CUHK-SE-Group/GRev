import concurrent.futures
import threading

from configs.config import logger
from gdb_clients import *
from copy import deepcopy
from mutator.query_transformer import QueryTransformer


def compare(result1, result2):
    data1 = deepcopy(result1)
    data2 = deepcopy(result2)
    return not (data1 == data2)


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
            logger.info(f"Neo4j exception: {e}. Triggering Query: {query}")
            return
        except Exception as e:
            logger.info(f"Unexpected exception: {e}. Triggering Query: {query}")
            return

        for step in range(0, 5):
            new_query = transformer.mutant_query_generator(query)
            try:
                result, query_time2 = client.run(new_query)
                result2 = result.data()
                if compare(result1, result2):
                    logger.warning(f"Logic inconsistency: Query1[{query}], Query2[{new_query}]")
                elif query_time1 > 1 and query_time2 > 1 and \
                        (query_time1 > 2 * query_time2 or query_time1 < 0.5 * query_time2):
                    logger.warning(
                        f"Performance inconsistency: Query1[{query}] using time {query_time1}, Query2[{new_query}] using time {query_time2}")
            except Neo4jError as e:
                logger.info(f"Neo4j exception: {e}. Triggering Query: {query}")
            except Exception as e:
                logger.info(f"Unexpected exception: {e}. Triggering Query: {query}")

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
