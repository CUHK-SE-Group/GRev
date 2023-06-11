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
    conf.logger.info("Initializing configuration...")
    create_statements, match_statements = conf.query_producer_func()
    conf.client.batch_run(create_statements)
    conf.logger.info("Formal test begin...")
    progress_bar = tqdm(total=len(match_statements))
    for query in match_statements:
        try:
            result1 = conf.client.run(query)
            for _ in range(0, conf.transform_times):
                new_query = conf.mutator_func(query)
                result2 = conf.client.run(new_query)
                conf.oracle_func(conf, result1, result2)
        except Exception as e:
            conf.logger.info(
                f"[{conf.database_name}][{conf.source_file}]Unexpected exception: {e}. \n Triggering Query: {query}")
            if conf.mode == 'live':
                conf.report(conf.report_token, f"[{conf.database_name}][{conf.source_file}]{e}, \nquery:", query)
        progress_bar.update(1)


# def prepare(conf: TestConfig):
#     conf.logger.info("Parsing input statements...")
#     create_statements, match_statements = parse_query_file(conf.source_file, conf.query_len)
#     conf.logger.info("Cleaning database...")
#     conf.client.clear()
#     conf.logger.info("Creating graph...")
#     conf.client.batch_run(create_statements)
#     return create_statements, match_statements


# def parse_query_file(logfile: str, query_len: int):
#     with open(logfile, 'r') as f:
#         content = f.read()

#     contents = content.strip().split('\n')
#     # 分离CREATE和MATCH语句
#     match_statements = contents[-query_len:]
#     create_statements = contents[4:-query_len]
#     return create_statements, match_statements


# def process_query(query: str, config: TestConfig):
#     result1, t1 = config.client.run(query)
#     for _ in range(0, config.transform_times):
#         new_query = config.mutator_func(query)
#         result2, t2 = config.client.run(new_query)
#         if not config.compare_function(result1, result2):
#             if config.mode == 'live':
#                 config.report(f"[{config.database_name}][{config.source_file}]Logic inconsistency",
#                               query + "\n" + new_query)
#             config.logger.warning(
#                 f"[{config.database_name}][{config.source_file}]Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
#             with open(config.logic_inconsistency_trace_file, mode='a', newline='') as file:
#                 writer = csv.writer(file, delimiter='\t')
#                 writer.writerow([config.database_name, config.source_file, query, new_query])
#         if t1 == 0:
#             t1 = 1
#         if t2 == 0:
#             t2 = 1
#         if t1 > config.performance_inconsistency_rate * t2 or config.performance_inconsistency_rate * t1 < t2:
#             if config.mode == 'live':
#                 config.report(
#                     f"[{config.database_name}][{config.source_file}]Performance inconsistency. Query1[{t1}ms, Query2[{t2}ms]] ",
#                     query + "\n" + new_query)
#             config.logger.warning(
#                 f"[{config.database_name}][{config.source_file}]Performance inconsistency. Query1[{t1}ms], Query2[{t2}ms] \n Query1: {query} \n Query2: {new_query}")
#     return True


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
