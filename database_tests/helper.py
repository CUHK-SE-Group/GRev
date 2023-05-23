import csv
import os
from abc import ABC

from tinydb import TinyDB, Query

from gdb_clients import GdbFactory
from mutator.query_transformer import QueryTransformer
from webhook.lark import post
from abc import ABC, abstractmethod


class TestConfig:
    def __init__(self, **kwargs):
        self.transformer = kwargs.get('transformer', QueryTransformer())
        self.mode = kwargs.get('mode', 'live')
        self.performance_inconsistency_rate = kwargs.get('performance_inconsistency_rate', 20)
        self.report = kwargs.get('report', post)
        self.transform_times = kwargs.get('transform_times', 5)

        self.client = kwargs.get('client')
        self.logger = kwargs.get('logger')
        self.compare_function = kwargs.get('compare_function')
        self.source_file = kwargs.get('source_file')
        self.logic_inconsistency_trace_file = kwargs.get('logic_inconsistency_trace_file')
        self.database_name = kwargs.get('database_name')
        self.query_len = kwargs.get('query_len')


class TesterAbs(ABC):
    @abstractmethod
    def single_file_testing(self, path):
        pass


def prepare(conf: TestConfig):
    conf.logger.info("Parsing input statements...")
    create_statements, match_statements = parse_query_file(conf.source_file, conf.query_len)
    conf.logger.info("Cleaning database...")
    conf.client.clear()
    conf.logger.info("Creating graph...")
    conf.client.batch_run(create_statements)
    return create_statements, match_statements


def parse_query_file(logfile: str, query_len: int):
    with open(logfile, 'r') as f:
        content = f.read()

    contents = content.strip().split('\n')
    # 分离CREATE和MATCH语句
    match_statements = contents[-query_len:]
    create_statements = contents[4:-query_len]
    return create_statements, match_statements


def process_query(query: str, config: TestConfig):
    client = config.client
    result1, t1 = client.run(query)

    for step in range(0, config.transform_times):
        new_query = config.transformer.mutant_query_generator(query)
        result2, t2 = client.run(new_query)
        if not config.compare_function(result1, result2):
            if config.mode == 'live':
                config.report(f"[{config.database_name}][{config.source_file}]Logic inconsistency",
                              query + "\n" + new_query)
            config.logger.warning(
                f"[{config.database_name}][{config.source_file}]Logic inconsistency. \n Query1: {query} \n Query2: {new_query}")
            with open(config.logic_inconsistency_trace_file, mode='a', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow([config.database_name, config.source_file, query, new_query])
        if t1 == 0:
            t1 = 1
        if t2 == 0:
            t2 = 1
        if t1 > config.performance_inconsistency_rate * t2 or config.performance_inconsistency_rate * t1 < t2:
            if config.mode == 'live':
                config.report(
                    f"[{config.database_name}][{config.source_file}]Performance inconsistency. Query1[{t1}ms, Query2[{t2}ms]] ",
                    query + "\n" + new_query)
            config.logger.warning(
                f"[{config.database_name}][{config.source_file}]Performance inconsistency. Query1[{t1}ms], Query2[{t2}ms] \n Query1: {query} \n Query2: {new_query}")
    return True


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
