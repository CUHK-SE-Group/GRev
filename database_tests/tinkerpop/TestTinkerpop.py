from collections import defaultdict
from database_tests.helper import *
from gdb_clients import *
from configs.conf import new_logger, config
import json


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
    lst1 = [i.__str__() for i in list1]
    lst2 = [i.__str__() for i in list2]
    lst1.sort()
    lst2.sort()
    return lst1 == lst2

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
            "query_time2": result2[1],
            })
        with open(conf.logic_inconsistency_trace_file, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow([conf.database_name, conf.source_file, conf.q1, conf.q2])


class TinkerTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile:str):
        def query_producer():
            if config.get('tinkerpop', 'input_mode') == "cypher":
                with open(logfile, 'r') as f:
                    content = f.read()
                contents = content.strip().split('\n')
                match_statements = contents[-5000:]
                create_statements = contents[4:-5000]
                return create_statements, match_statements
            elif config.get('tinkerpop', 'input_mode') == "gremlin":
                with open(logfile, "r", encoding = "utf-8") as f:
                    create_statements = f.read().strip().split('\n')
                with open(logfile.replace("create", "query"), "r", encoding = "utf-8") as f:
                    match_statements = json.load(f)
                return create_statements, match_statements
        
        logger = new_logger("logs/tinkerpop.log", True)
        conf = TestConfig(
            client=Tinkerpop(),
            logger=logger,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/tinkerpop_logic_error.tsv',
            database_name=self.database,
            query_producer_func=query_producer,
            oracle_func=oracle,
            report_token=config.get('lark', 'tinkerpop')
        )

        general_testing_procedure(conf)
        return True


def schedule():
    # gremlin_scheduler(config.get('tinkerpop', 'input_path'), TinkerTester(f"tinkerpop"), "tinkerpop")
    scheduler(config.get('tinkerpop', 'input_path'), TinkerTester(f"tinkerpop"), "tinkerpop")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = TinkerTester('tinkerpop')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
