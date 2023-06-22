import csv
import os
from abc import ABC
from tqdm import tqdm
from tinydb import TinyDB, Query
from logging import Logger
from gdb_clients import GdbFactory
from mutator.query_transformer import QueryTransformer
from webhook.lark import post
from abc import ABC, abstractmethod
from typing import Callable
import redis
import traceback

class TestConfig:
    def __init__(self, **kwargs):

        self.mode = kwargs.get('mode', 'live')
        self.report = kwargs.get('report', post)
        self.report_token = kwargs.get('report_token')
        self.transform_times = kwargs.get('transform_times', 5)

        self.client: GdbFactory = kwargs.get('client')
        self.logger: Logger = kwargs.get('logger')
        self.source_file = kwargs.get('source_file')
        self.logic_inconsistency_trace_file = kwargs.get('logic_inconsistency_trace_file')
        self.database_name = kwargs.get('database_name')

        self.mutator_func: Callable[[str], str] = kwargs.get('mutator_func', QueryTransformer().mutant_query_generator)
        self.query_producer_func = kwargs.get('query_producer_func', lambda: ([], []))
        self.oracle_func: Callable[[TestConfig, any, any], None] = kwargs.get("oracle_func")

        # temp val for consistency checker
        self.q1 = None
        self.q2 = None


class TesterAbs(ABC):
    @abstractmethod
    def single_file_testing(self, path):
        pass

def general_testing_procedure(conf: TestConfig):
    create_statements, match_statements = conf.query_producer_func()
    conf.client.clear()
    conf.client.batch_run(create_statements)
    progress_bar = tqdm(total=len(match_statements))
    for query in match_statements:
        try:
            if isinstance(query, dict):
                result1 = conf.client.run(query['Query1'])
                result2 = conf.client.run(query['Query2'])
                conf.q1 = query['Query1']
                conf.q2 = query['Query2']
                conf.oracle_func(conf, result1, result2)
            else:
                result1 = conf.client.run(query)
                for _ in range(0, conf.transform_times):
                    new_query = conf.mutator_func(query)
                    result2 = conf.client.run(new_query)
                    conf.q1 = query
                    conf.q2 = new_query
                    conf.oracle_func(conf, result1, result2)
        except redis.exceptions.ResponseError as e:
            tb_str = traceback.format_tb(e.__traceback__)
            conf.logger.info({
                "database_name": conf.database_name,
                "source_file": conf.source_file,
                "tag": "exception",
                "exception_content": e.__str__(),
                "query1": conf.q1,
                "query2": conf.q2,
                "traceback": tb_str
                })
        except ValueError as e:
            tb_str = traceback.format_tb(e.__traceback__)
            conf.logger.info({
                "database_name": conf.database_name,
                "source_file": conf.source_file,
                "tag": "exception",
                "exception_content": e.__str__(),
                "query1": conf.q1,
                "query2": conf.q2,
                "traceback": tb_str
                })
        except Exception as e:
            tb_str = traceback.format_tb(e.__traceback__)
            conf.logger.info({
                "database_name": conf.database_name,
                "source_file": conf.source_file,
                "tag": "exception",
                "exception_content": e.__str__(),
                "query1": conf.q1,
                "query2": conf.q2,
                "traceback": tb_str
                })
            if conf.mode == 'live':
                conf.report(conf.report_token, f"[{conf.database_name}][{conf.source_file}]", f"exception: \n{e} \nquery:\n{query}")
        progress_bar.update(1)

def scheduler(folder_path, tester: TesterAbs, database):
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            if 'cur.log' in file:
                file_path = os.path.join(dirpath, file)
                file_paths.append(file_path)

    sorted_file_paths = sorted(file_paths)

    for file_path in sorted_file_paths:
        db = TinyDB('db.json')
        table = db.table(database)
        session = Query()
        res = table.search(session.FileName == file_path)
        if not res:
            table.insert({'FileName': file_path, 'status': 'doing'})
            success = tester.single_file_testing(file_path)
            if success:
                table.update({'status': 'done'}, session.FileName == file_path)
            else:
                table.remove(session.FileName == file_path)



def gremlin_scheduler(folder_path, tester: TesterAbs, database):
    for i in range(100):
        file_path = os.path.join(folder_path, f'create-{i}.log')
        db = TinyDB('db.json')
        table = db.table(database)
        session = Query()
        res = table.search(session.FileName == file_path)
        if not res:
            table.insert({'FileName': file_path, 'status': 'doing'})
            success = tester.single_file_testing(file_path)
            if success:
                table.update({'status': 'done'}, session.FileName == file_path)
            else:
                table.remove(session.FileName == file_path)