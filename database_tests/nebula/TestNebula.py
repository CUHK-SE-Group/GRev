import csv
from ngql.query_generator import *
from database_tests.helper import *
from gdb_clients import *
from configs.conf import *
import time


def compare(result1, result2):
    """Returns None iff the two results are identical"""
    lst1 = [v.__str__() for _, v in result1.items()]
    lst2 = [v.__str__() for _, v in result2.items()]
    lst1.sort()
    lst2.sort()

    if lst1 == lst2:
        return None
    elif bool(lst1) != bool(lst2):
        return "One is empty and the other is not"
    elif len(lst1) != len(lst2):
        return "Both non-empty but of unequal lengths"
    else:
        return "Have equal lengths but not identical"

# result: is returned by client.run()
def oracle(conf: TestConfig, result1, result2):
    num1 = sum([len(v) for _, v in result1[0].items()])
    num2 = sum([len(v) for _, v in result2[0].items()])
    result_compare = compare(result1[0], result2[0])
    if result_compare:
        if conf.mode == 'live':
            conf.report(conf.report_token, f"[{conf.database_name}][{conf.source_file}]Logic inconsistency",
                        conf.q1 + "\n" + conf.q2)
            conf.logger.warning({
                "database_name": conf.database_name,
                "source_file": conf.source_file,
                "tag": "logic_inconsistency",
                "query1": conf.q1,
                "query2": conf.q2,
                "query_res1": result1[0].__str__() if num1<100 else "",
                "query_res2": result2[0].__str__() if num2<100 else "",
                "query_time1": result1[1],
                "query_time2": result2[1],
            })
        with open(conf.logic_inconsistency_trace_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([conf.database_name, conf.source_file, conf.q1, conf.q2])
    big = max(result1[1], result2[1])
    small = min(result1[1], result2[1])
    heap = MaxHeap("logs/nebula_performance.json",10)
    metric = big/(small+100)
    if metric > 2:
        heap.insert(metric)
    threshold = heap.get_heap()
    if metric in threshold:
        if conf.mode == 'live':
            conf.report(conf.report_token,f"[{conf.database_name}][{conf.source_file}][{big}ms,{small}ms]Performance inconsistency",
                        conf.q1 + "\n" + conf.q2)
        conf.logger.warning({
                "database_name": conf.database_name,
                "source_file": conf.source_file,
                "tag": "performance_inconsistency",
                "query1": conf.q1,
                "query2": conf.q2,
                "query_res1": result1[0].__str__() if num1<100 else "",
                "query_res2": result2[0].__str__() if num2<100 else "",
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
            with open(f"./query_producer/interesting.txt", 'w') as f:
                for statement_pair in match_statements:
                    print(statement_pair, file=f)
            contents = content.strip().split('\n')
            return contents, match_statements
        logger = new_logger("logs/nebula.log", False)
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
