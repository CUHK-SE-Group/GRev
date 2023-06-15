from database_tests.helper import *
from configs.conf import new_logger, config
from gdb_clients.mem_graph import MemGraph
import csv


def compare(list1, list2):
    if len(list1) != len(list2):
        return False
    t1 = [i.__str__() for i in list1]
    t2 = [i.__str__() for i in list2]
    t1.sort()
    t2.sort()
    return t1 == t2

def oracle(conf: TestConfig, result1, result2):
    if not compare(result1[0], result2[0]):
        if conf.mode == 'live':
            conf.report(conf.report_token,f"[{conf.database_name}][{conf.source_file}]Logic inconsistency",
                        conf.q1 + "\n" + conf.q2)
        conf.logger.warning({
            "database_name": conf.database_name,
            "source_file": conf.source_file,
            "tag": "logic_inconsistency",
            "query1": conf.q1,
            "query2": conf.q2,
            "query_res1": result1[0].__str__(),
            "query_res2": result2[0].__str__(),
            "query_time1": result1[1],
            "query_time1": result2[1],
            })
        with open(conf.logic_inconsistency_trace_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([conf.database_name, conf.source_file, conf.q1, conf.q2])
    big = max(result1[1], result2[1])
    small = min(result1[1], result2[1])
    if big > 5 * small and small>100:
        if conf.mode == 'live':
            conf.report(conf.report_token, f"[{conf.database_name}][{conf.source_file}][{big}ms,{small}ms]Performance inconsistency",
                        conf.q1 + "\n" + conf.q2)
        conf.logger.warning({
            "database_name": conf.database_name,
            "source_file": conf.source_file,
            "tag": "performance_inconsistency",
            "query1": conf.q1,
            "query2": conf.q2,
            "query_res1": result1[0].__str__(),
            "query_res2": result2[0].__str__(),
            "query_time1": result1[1],
            "query_time1": result2[1],
        })


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
        
        logger = new_logger("logs/memgraph.log", True)
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
