from collections import defaultdict
from database_tests.helper import *
from gdb_clients import *
from configs.conf import new_logger, config
import csv

def list_to_dict(lst):
    result = defaultdict(int)
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

def oracle(conf: TestConfig, result1, result2):
    if not compare(result1[0], result2[0]):
        if conf.mode == 'live':
            conf.report(conf.report_token,f"[{conf.database_name}][{conf.source_file}]Logic inconsistency",
                        conf.q1 + "\n" + conf.q2)
        conf.logger.warning(
                f"[{conf.database_name}][{conf.source_file}]Logic inconsistency. \n Query1: {conf.q1} \n Query2: {conf.q2}")
        with open(conf.logic_inconsistency_trace_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([conf.database_name, conf.source_file, conf.q1, conf.q2])


class RedisTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        def query_producer():
            with open(logfile, 'r') as f:
                content = f.read()
            contents = content.strip().split('\n')
            match_statements = contents[-5000:]
            create_statements = contents[4:-5000]
            return create_statements, match_statements
        
        logger = new_logger("logs/redis.log")
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=Redis(config.get("redis", 'uri'), self.database),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/redis_logic_error.tsv',
            database_name='redis',
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark', 'redis')
        )
        general_testing_procedure(conf)
        return True


def schedule():
    scheduler(config.get('redis', 'input_path'), RedisTester(f"redis_misc"), "redis")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = RedisTester('dev_graph')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
