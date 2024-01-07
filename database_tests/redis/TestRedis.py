from database_tests.helper import *
from gdb_clients import *
from configs.conf import new_logger, config
import csv
from mutator.redis.query_transformer import QueryTransformer

def deep_sort(obj):
    if isinstance(obj, list):
        return sorted((deep_sort(sub) for sub in obj), key=str)
    else:
        return str(obj)
    
def compare(list1, list2):
    if len(list1) != len(list2):
        return False
    if len(list1) >= 9000:
        return True
    lst1 = deep_sort(list1)
    lst2 = deep_sort(list2)
    lst1.sort()
    lst2.sort()
    return lst1 == lst2

total = 0
def oracle(conf: TestConfig, result1, result2):
    global total
    if not compare(result1[0], result2[0]):
        conf.num_logic += 1
        total += 1
        print(f"================={total}==================")
        if conf.mode == 'live':
            conf.report(conf.report_token,f"[{conf.database_name}][{conf.source_file}]Logic inconsistency",
                        f"{conf.q1}\n{conf.q2}")
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
            writer.writerow([conf.database_name, conf.source_file, conf.q1, conf.q2])

    big = max(result1[1], result2[1])
    small = min(result1[1], result2[1])
    C1, C2 = 0.8, 1000.0
    V1, V2 = (big - small) / big, big - small
    if V1 >= C1 and V2 >= C2:
        total+=1
        print(f"================={total}==================")
        conf.num_performance += 1
        print(f'detected performance issue; current # = {conf.num_performance}')
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


class RedisTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        def query_producer():
            with open(logfile, 'r') as f:
                content = f.read()
            contents = content.strip().split('\n')
            query_statements = contents[-5000:]
            create_statements = contents[4:-5000]
            return create_statements, query_statements

        logger = new_logger("logs/redis.log", True)
        qt = QueryTransformer()
        conf = TestConfig(
            client=Redis(uri="localhost", database=self.database),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/redis_logic_error.tsv',
            database_name='redis',
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark', 'redis'),
            mutator_func=qt.mutant_query_generator
        )
        general_testing_procedure(conf)
        return True

    def single_file_testing_alt(self, logfile, create_statements, query_statements):
        def query_producer():
            return create_statements, query_statements

        logger = new_logger("logs/redis.log")
        qt = QueryTransformer()
        conf = TestConfig(
            # client=Redis(config.get("redis", "uri"), self.database),
            client=Redis(uri="localhost", database=self.database),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/redis_logic_error.tsv',
            database_name='redis',
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark', 'redis'),
            mutator_func=qt.mutant_query_generator
        )
        general_testing_procedure(conf)
        # return conf.num_bug_triggering
        return conf.num_logic, conf.num_performance


def schedule():
    scheduler(config.get('redis', 'input_path'), RedisTester(f"redis_misc"), "redis")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = RedisTester('dev_graph')
        Tester.single_file_testing("./query_producer/logs/composite/database263-cur.log")
    else:
        schedule()
