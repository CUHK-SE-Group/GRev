import concurrent.futures
import random
import threading
from concurrent.futures import CancelledError
from copy import deepcopy
from tinydb import TinyDB, Query
import os
import configs
from gdb_clients import *
from configs.config import logger
from mutator.query_transformer import QueryTransformer
from compare.hash_nested_dict import hash_dictionary
from webhook.lark import post
import subprocess

stop_event = threading.Event()


def compare(result1, result2):
    data1 = deepcopy(result1)
    data2 = deepcopy(result2)
    if len(data1) != len(data2):
        return 0
    return not (sorted([hash_dictionary(x) for x in data1]) == sorted([hash_dictionary(x) for x in data2]))


class Neo4jTester():
    def __init__(self, database):
        temp_conn = Neo4j(configs.neo4j_uri, configs.neo4j_username, configs.neo4j_passwd, '')
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
            self.connections[thread_id] = Neo4j(configs.neo4j_uri, configs.neo4j_username, configs.neo4j_passwd,
                                                self.database)
        return self.connections[thread_id]

    def process_query(self, query: str, transformer: QueryTransformer, logfile):
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
                    post(f"[{self.database}][{logfile}]Logic inconsistency", query)
                logger.warn(f"[{self.database}][{logfile}]Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
                return False
            elif query_time1 > 1000 and query_time2 > 1000 and \
                    (query_time1 > 5 * query_time2 or query_time1 < 0.2 * query_time2):
                if configs.global_env == 'live':
                    post(f"[{self.database}][{logfile}]Performance inconsistency",
                         f"[Query1: {query}\n using time: {query_time1}ms  \n Query2: {new_query} \n using time: {query_time2}ms")
                logger.info(
                    f"[{self.database}][{logfile}]Performance inconsistency. \n Query1: {query} \n using time: {query_time1}ms \n Query2: {new_query} \n using time: {query_time2}ms")
                return False
        return True

    def single_file_testing(self, logfile):
        client = Neo4j(configs.neo4j_uri, configs.neo4j_username, configs.neo4j_passwd, self.database)

        with open(logfile, 'r') as f:
            content = f.read()

        contents = content.strip().split('\n')
        # 分离CREATE和MATCH语句
        match_statements = contents[-5000:]
        create_statements = contents[4:-5000]

        client.create_graph(create_statements)
        client = None
        Q = QueryTransformer()
        cnt = 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=configs.concurrency) as executor:
            futures = {executor.submit(self.process_query, query, Q, logfile): query for query in match_statements}

            for future in concurrent.futures.as_completed(futures):
                print(cnt)
                cnt += 1
                try:
                    query = futures[future]
                    result = future.result(configs.timeout)
                except CancelledError as e:
                    logger.info(f"[{self.database}][{logfile}] Execute cancelled: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post(f'[{self.database}][{logfile}]Execute cancelled', query)
                except TimeoutError as e:
                    logger.info(f"[{self.database}][{logfile}]Execute timeout: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post(f'[{self.database}][{logfile}]Execute timeout', query)
                except Neo4jError as e:
                    logger.info(f"[{self.database}][{logfile}]Neo4j exception: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post(f'[{self.database}][{logfile}]{e.title}.{e.category}.{e.classification}', query)
                except Exception as e:
                    logger.info(f"[{self.database}][{logfile}]Unexpected exception: {e}. \n Triggering Query: {query}")
                    if configs.global_env == 'live':
                        post(f"[{self.database}][{logfile}]Unknown Exception", query)
        return True


def producer():
    current_dir = os.getcwd()
    new_dir = "query_producer"
    os.chdir(new_dir)
    command = ['java', '-jar', 'GDsmith.jar', '--num-tries', '1', '--num-queries', '5000', '--algorithm',
               'compared3', '--num-threads', '12', 'composite']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"执行命令时出现错误: {error.decode('utf-8')}")
    else:
        print(f"命令执行成功，输出信息: {output.decode('utf-8')}")


def scheduler():
    folder_path = 'query_producer/logs/composite'
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            if 'cur.log' in file:
                file_path = os.path.join(dirpath, file)
                file_paths.append(file_path)

    sorted_file_paths = sorted(file_paths)

    idx = random.randint(0, 1000000000000)
    t = Neo4jTester(f"pattern{idx}")
    for file_path in sorted_file_paths:
        db = TinyDB('db.json')
        table = db.table('pattern_transformer')
        session = Query()
        res = table.search(session.FileName == file_path)
        if not res:
            table.insert({'FileName': file_path, 'status': 'doing'})
            success = t.single_file_testing(file_path)
            if success:
                table.update({'status': 'done'}, session.FileName == file_path)
            else:
                table.remove(session.FileName == file_path)


if __name__ == "__main__":
    if configs.global_env == "debug":
        Tester = Neo4jTester('test4')
        Tester.single_file_testing("query_file/database0-cur.log")
        stop_event.set()
    else:
        scheduler()
