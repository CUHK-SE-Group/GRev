from collections import defaultdict
from tqdm import tqdm
import redis
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


class RedisTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        logger = new_logger("logs/redis.log")
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=Redis(config.get("redis", 'uri'), self.database),
            logger=logger,
            compare_function=compare,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/redis_logic_error.tsv',
            database_name='redis',
            query_len=5000
        )

        create_statements, match_statements = prepare(conf)
        logger.info("Formal test begin...")
        progress_bar = tqdm(total=len(match_statements))
        for query in match_statements:
            env = config.get("GLOBAL", "env")
            try:
                process_query(query, conf)
            except redis.exceptions.ConnectionError as e:
                logger.info(f"[{self.database}][{logfile}]ConnectionError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]ConnectionError', query)
            except redis.exceptions.TimeoutError as e:
                logger.info(f"[{self.database}][{logfile}]TimeoutError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]TimeoutError', query)
            except redis.exceptions.InvalidResponse as e:
                logger.info(f"[{self.database}][{logfile}]InvalidResponse: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]InvalidResponse', query)
            except redis.exceptions.ResponseError as e:
                logger.info(f"[{self.database}][{logfile}]ResponseError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]ResponseError', query)
            except redis.exceptions.DataError as e:
                logger.info(f"[{self.database}][{logfile}]DataError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]DataError', query)
            except redis.exceptions.PubSubError as e:
                logger.info(f"[{self.database}][{logfile}]PubSubError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]PubSubError', query)
            except redis.exceptions.WatchError as e:
                logger.info(f"[{self.database}][{logfile}]WatchError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f'[{self.database}][{logfile}]WatchError', query)
            except TypeError as e:
                logger.info(f"[{self.database}][{logfile}]TypeError: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f"[{self.database}][{logfile}]TypeError", query)
            except Exception as e:
                logger.info(f"[{self.database}][{logfile}]Unexpected exception: {e}. \n Triggering Query: {query}")
                if env == 'live':
                    post(f"[{self.database}][{logfile}]Unknown Exception", query)
            progress_bar.update(1)
        return True


def schedule():
    scheduler(config.get('redis', 'input_path'), RedisTester(f"redis_misc"), "redis")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = RedisTester('dev_graph')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
