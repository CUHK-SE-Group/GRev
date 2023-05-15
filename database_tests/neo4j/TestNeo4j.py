import random
import threading
from concurrent.futures import CancelledError
from copy import deepcopy
from neo4j.exceptions import Neo4jError
from tqdm import tqdm
from database_tests.helper import TestConfig, parse_query_file, prepare, process_query, scheduler, TesterAbs
from gdb_clients import *
from configs.conf import logger, config
from compare.hash_nested_dict import hash_dictionary
from webhook.lark import post


def compare(result1, result2):
    data1 = deepcopy(result1)
    data2 = deepcopy(result2)
    if len(data1) != len(data2):
        return False
    return (sorted([hash_dictionary(x) for x in data1]) == sorted([hash_dictionary(x) for x in data2]))


class Neo4jTester(TesterAbs):
    def __init__(self, database):
        temp_conn = Neo4j(config.get('neo4j', 'uri'), config.get('neo4j', 'username'), config.get('neo4j', 'passwd'),
                          '')
        logger.info("Initializing dabtases...")
        result, _ = temp_conn.run("SHOW DATABASES")
        database_names = [record['name'] for record in result]
        # 检查指定的数据库是否在数据库名称列表中
        if database in database_names:
            logger.info("The database exists...")
        else:
            logger.info("Creating database...")
            temp_conn.run(f"CREATE DATABASE {database}")
        temp_conn = None
        self.connections = {}
        self.database = database

    def get_connection(self):
        thread_id = threading.get_ident()
        if thread_id not in self.connections:
            self.connections[thread_id] = Neo4j(config.get("neo4j", 'uri'), config.get('neo4j', 'username'),
                                                config.get('neo4j', 'passwd'),
                                                self.database)
        return self.connections[thread_id]

    def single_file_testing(self, logfile):
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=Neo4j(config.get("neo4j", 'uri'), config.get('neo4j', 'username'), config.get('neo4j', 'passwd'),
                         self.database),
            logger=logger,
            compare_function=compare,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/neo4j_logic_error.tsv',
            database_name='neo4j',
            query_len=5000,
            mode="debug",
            performance_inconsistency_rate=10000
        )

        create_statements, match_statements = prepare(conf)
        logger.info("Formal test begin...")
        progress_bar = tqdm(total=len(match_statements))
        env = config.get("GLOBAL", 'env')
        for query in match_statements:
            try:
                process_query(query, conf)
            except CancelledError as e:
                logger.info(f"[{self.database}][{logfile}] Execute cancelled: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]Execute cancelled', query)
            except TimeoutError as e:
                logger.info(f"[{self.database}][{logfile}]Execute timeout: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]Execute timeout', query)
            except Neo4jError as e:
                logger.info(f"[{self.database}][{logfile}]Neo4j exception: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]{e.title}.{e.category}.{e.classification}', query)
            except Exception as e:
                logger.info(f"[{self.database}][{logfile}]Unexpected exception: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f"[{self.database}][{logfile}]Unknown Exception", query)
            progress_bar.update(1)
        return True


def schedule():
    idx = random.randint(0, 1000000000000)
    scheduler(config.get('neo4j', 'input_path'), Neo4jTester(f"pattern{idx}"), 'neo4j')


if __name__ == "__main__":
    if config.get("GLOBAL", 'env') == "debug":
        Tester = Neo4jTester('test4')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
