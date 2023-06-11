from tqdm import tqdm
from database_tests.helper import *
from configs.conf import new_logger, config
from gdb_clients.mem_graph import MemGraph
from webhook.lark import post
import csv


def sort_key(dictionary: dict):
    # 根据字典中的 'key' 键进行排序
    return '{' + ', '.join(f"{repr(key)}: {dictionary[key]}" for key in sorted(dictionary.keys())) + '}'


def compare(list1, list2):
    if len(list1) != len(list2):
        return False
    t1 = sorted(list1, key=sort_key)
    t2 = sorted(list2, key=sort_key)
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

class MemgraphTester(TesterAbs):
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
        
        logger = new_logger("logs/memgraph.log")
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=MemGraph(),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/memgraph_logic_error.tsv',
            database_name='memgraph',
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark', 'memgraph')
        )

        general_testing_procedure(conf)
        return True


def schedule():
    scheduler(config.get('memgraph', 'input_path'), MemgraphTester(f"memgraph_misc"), "memgraph")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = MemgraphTester('dev_graph')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
