import csv
from ngql.query_generator import *
from database_tests.helper import TestConfig, general_testing_procedure, scheduler, TesterAbs
from gdb_clients import *
from configs.conf import *
import time


def compare(result1, result2):
    if len(result1) != len(result2):
        return False
    lst1 = [i.__str__() for i in result1]
    lst2 = [i.__str__() for i in result2]
    lst1.sort()
    lst2.sort()
    return lst1 == lst2

# result: is returned by client.run()
def oracle(conf: TestConfig, result1, result2):
    if not compare(result1[0], result2[0]):
        if conf.mode == 'live':
            conf.report(f"[{config.database_name}][{config.source_file}]Logic inconsistency",
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
                "query_time2": result2[1],
            })
        with open(conf.logic_inconsistency_trace_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([config.database_name, config.source_file, conf.q1, conf.q2])
    big = max(result1[1], result2[1])
    small = min(result1[1], result2[1])
    if big > 5 * small and small>20:
        if conf.mode == 'live':
            conf.report(conf.report_token,f"[{conf.database_name}][{conf.source_file}][{big}ms,{small}ms]Performance inconsistency",
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
                "query_time2": result2[1],
            })



class NebulaTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        t = time.time()
        logfile = f"./query_producer/nebula/{t}.log"
        def query_producer():
            generator = QueryGenerator(f"./query_producer/nebula/{t}.log")
            with open(f"./query_producer/nebula/{t}.log", 'r') as f:
                content = f.read()
                f.close()
            match_statements = [generator.gen_query() for i in range(200)]
            contents = content.strip().split('\n')
            return contents, match_statements
        logger = new_logger("logs/nebula.log", True)
        conf = TestConfig(
            client=Nebula(self.database),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/nebula_logic_error.tsv',
            database_name='nebula',
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark','nebula')
        )
        general_testing_procedure(conf)


def schedule():
    scheduler(config.get('nebula', 'input_path'), NebulaTester("nebulatesting"), 'nebula')


if __name__ == "__main__":
    if config.get("GLOBAL", 'env') == "debug":
        pass
    else:
        schedule()
