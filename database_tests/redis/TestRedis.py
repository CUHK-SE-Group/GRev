import csv
import threading
from collections import defaultdict

import redis
from tinydb import TinyDB, Query
import os
import configs
from gdb_clients import *
from configs.config import logger
from mutator.query_transformer import QueryTransformer
from webhook.lark import post

stop_event = threading.Event()


def list_to_dict(lst):
    # 定义一个defaultdict，用于创建一个默认值为0的字典
    result = defaultdict(int)
    # 对于列表中的每个元素，如果它是一个列表，则递归调用list_to_dict函数
    # 如果不是列表，则将其作为键添加到字典中，并增加其出现次数
    for elem in lst:
        if isinstance(elem, list):
            nested_dict = list_to_dict(elem)
            for key, value in nested_dict.items():
                result[key] += value
        else:
            result[elem] += 1
    return dict(result)


def compare(list1, list2):
    if len(list1) != len(list2):
        return False
    t1 = list_to_dict(list1)
    t2 = list_to_dict(list2)
    return t1 == t2


class RedisTester:
    def __init__(self, database):
        self.connection = Redis("10.20.10.27", database)
        self.database = database

    def get_connection(self):
        return self.connection

    def process_query(self, query: str, transformer: QueryTransformer, logfile):
        if stop_event.is_set():
            return False
        client = self.get_connection()
        result1, t1 = client.run(query)

        for step in range(0, 5):
            if stop_event.is_set():
                return False
            new_query = transformer.mutant_query_generator(query)
            result2, t2 = client.run(new_query)
            if not compare(result1, result2):
                if configs.global_env == 'live':
                    post(f"[{self.database}][{logfile}]Logic inconsistency", query + "\n" + new_query)
                logger.warning(
                    f"[{self.database}][{logfile}]Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
                # 打开CSV文件进行追加，如果文件不存在则创建
                with open('logic_error.tsv', mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter='\t')
                    writer.writerow([self.database, logfile, query, new_query])
                return False
            if t1 > 20 * t2 or t1 < 0.05 * t2:
                if configs.global_env == 'live':
                    post(f"[{self.database}][{logfile}]Performance inconsistency. Query1[{t1}ms, Query2[{t2}ms]] ", query + "\n" + new_query)
                logger.warning(
                    f"[{self.database}][{logfile}]Performance inconsistency. Query1[{t1}ms, Query2[{t2}ms]] \n Query1: {query} \n Query2: {new_query}")
        return True

    def single_file_testing(self, logfile):
        client = Redis("10.20.10.27", self.database)
        client.clear()

        with open(logfile, 'r') as f:
            content = f.read()

        contents = content.strip().split('\n')
        # 分离CREATE和MATCH语句
        match_statements = contents[-configs.query_len:]
        create_statements = contents[4:-configs.query_len]

        client.create_graph(create_statements)
        client = None
        Q = QueryTransformer()
        cnt = 1
        for query in match_statements:
            print(cnt)
            cnt += 1
            try:
                result = self.process_query(query, Q, logfile)
            except redis.exceptions.ConnectionError as e:
                logger.info(f"[{self.database}][{logfile}]ConnectionError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]ConnectionError', query)
            except redis.exceptions.TimeoutError as e:
                logger.info(f"[{self.database}][{logfile}]TimeoutError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]TimeoutError', query)
            except redis.exceptions.InvalidResponse as e:
                logger.info(f"[{self.database}][{logfile}]InvalidResponse: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]InvalidResponse', query)
            except redis.exceptions.ResponseError as e:
                logger.info(f"[{self.database}][{logfile}]ResponseError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]ResponseError', query)
            except redis.exceptions.DataError as e:
                logger.info(f"[{self.database}][{logfile}]DataError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]DataError', query)
            except redis.exceptions.PubSubError as e:
                logger.info(f"[{self.database}][{logfile}]PubSubError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]PubSubError', query)
            except redis.exceptions.WatchError as e:
                logger.info(f"[{self.database}][{logfile}]WatchError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f'[{self.database}][{logfile}]WatchError', query)
            except TypeError as e:
                logger.info(f"[{self.database}][{logfile}]TypeError: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f"[{self.database}][{logfile}]TypeError", query)
            except Exception as e:
                logger.info(f"[{self.database}][{logfile}]Unexpected exception: {e}. \n Triggering Query: {query}")
                if configs.global_env == 'live':
                    post(f"[{self.database}][{logfile}]Unknown Exception", query)
        return True


def scheduler():
    folder_path = configs.input_path
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            if 'cur.log' in file:
                file_path = os.path.join(dirpath, file)
                file_paths.append(file_path)

    sorted_file_paths = sorted(file_paths)

    t = RedisTester(f"test_graph")
    for file_path in sorted_file_paths:
        db = TinyDB('db.json')
        table = db.table('redis')
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
        Tester = RedisTester('test_graph')
        Tester.single_file_testing("query_file/database0-cur.log")
        stop_event.set()
    else:
        scheduler()
