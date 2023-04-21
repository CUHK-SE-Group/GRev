import concurrent.futures
import threading
from concurrent.futures import CancelledError
from copy import deepcopy

import configs
from gdb_clients import *
from configs.config import logger
from mutator.query_transformer import QueryTransformer
from compare.hash_nested_dict import hash_dictionary
from webhook.lark import post

stop_event = threading.Event()


def compare(result1, result2):
    data1 = deepcopy(result1)
    data2 = deepcopy(result2)
    if len(data1) != len(data2):
        return 0
    return not (sorted([hash_dictionary(x) for x in data1]) == sorted([hash_dictionary(x) for x in data2]))


class Neo4jTester():
    def __init__(self):
        self.connections = {}

    def get_connection(self):
        thread_id = threading.get_ident()
        if thread_id not in self.connections:
            self.connections[thread_id] = Neo4j(configs.neo4j_uri, configs.neo4j_username, configs.neo4j_passwd)
        return self.connections[thread_id]

    def process_query(self, query: str, transformer: QueryTransformer):
        if stop_event.is_set():
            return False
        client = self.get_connection()
        result, query_time1 = client.run(query)
        result1 = result

        for step in range(0, 5):
            if stop_event.is_set():
                return False
            new_query = transformer.mutant_query_generator(query)
            result, query_time2 = client.run(new_query)
            result2 = result
            if compare(result1, result2):
                if configs.global_env == 'live':
                    post("Logic inconsistency", query)
                logger.warn(f"Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
                return False
            elif query_time1 > 1 and query_time2 > 1 and \
                    (query_time1 > 2 * query_time2 or query_time1 < 0.5 * query_time2):
                if configs.global_env == 'live':
                    post("Performance inconsistency", f"Query1: {query}\n using time: {query_time1}  \n Query2: {new_query} \n using time: {query_time2}")
                logger.info(
                    f"Performance inconsistency. \n Query1: {query} \n using time: {query_time1} \n Query2: {new_query} \n using time: {query_time2}")
                return False
        return True

    def Testing(self, create_file, query_file):
        client = Neo4j(configs.neo4j_uri, configs.neo4j_username, configs.neo4j_passwd)
        client.create_graph(create_file)
        Q = QueryTransformer()
        with open(query_file, 'r') as f:
            queries = f.readlines()
            queries = [query.replace('\n', '') for query in queries]
        cnt = 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=configs.concurrency) as executor:
            futures = {executor.submit(self.process_query, query, Q): query for query in queries}

            for future in concurrent.futures.as_completed(futures):
                print(cnt)
                cnt += 1
                try:
                    query = futures[future]
                    result = future.result(configs.timeout)
                except CancelledError as e:
                    logger.info(f"Execute cancelled: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post('Execute cancelled', query)
                except TimeoutError as e:
                    logger.info(f"Execute timeout: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post('Execute timeout', query)
                except Neo4jError as e:
                    logger.info(f"Neo4j exception: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post(f'{e.title}.{e.category}.{e.classification}', query)
                except Exception as e:
                    logger.info(f"Unexpected exception: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post("Unknown Exception", query)


if __name__ == "__main__":
    Tester = Neo4jTester()
    Tester.Testing("query_file/create.log", "query_file/query.log")
    print('主线程退出')
    stop_event.set()
