from collections import defaultdict
from tqdm import tqdm
from database_tests.helper import parse_query_file, TestConfig, process_query, scheduler, TesterAbs, prepare
from gdb_clients import *
from configs.conf import new_logger, config
from webhook.lark import post

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
    t1 = list_to_dict(list1)
    t2 = list_to_dict(list2)
    return t1 == t2


class AgeTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        logger = new_logger("logs/age.log", True)
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=AgeDB(),
            logger=logger,
            compare_function=compare,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/age_logic_error.tsv',
            database_name='age',
            query_len=5000
        )

        create_statements, match_statements = prepare(conf)
        logger.info("Formal test begin...")
        progress_bar = tqdm(total=len(match_statements))
        for query in match_statements:
            env = config.get("GLOBAL", "env")
            try:
                process_query(query, conf)
            except Exception as e:
                logger.info(f"[{self.database}][{logfile}]Unexpected exception: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f"[{self.database}][{logfile}]Unknown Exception", query)
            progress_bar.update(1)
        return True


def schedule():
    scheduler(config.get('age', 'input_path'), AgeTester(f"age"), "age")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = AgeTester('age')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
