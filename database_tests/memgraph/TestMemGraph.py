from tqdm import tqdm
import redis
from database_tests.helper import parse_query_file, TestConfig, process_query, scheduler, TesterAbs, prepare
from configs.conf import new_logger, config
from gdb_clients.mem_graph import MemGraph
from webhook.lark import post


def sort_key(dictionary: dict):
    # 根据字典中的 'key' 键进行排序
    return '{' + ', '.join(f"{repr(key)}: {dictionary[key]}" for key in sorted(dictionary.keys())) + '}'


def compare(list1, list2):
    if len(list1) != len(list2):
        return False
    t1 = sorted(list1, key=sort_key)
    t2 = sorted(list2, key=sort_key)
    return t1 == t2


class MemgraphTester(TesterAbs):
    def __init__(self, database):
        self.database = database

    def single_file_testing(self, logfile):
        logger = new_logger("logs/memgraph.log")
        logger.info("Initializing configuration...")
        conf = TestConfig(
            client=MemGraph(),
            logger=logger,
            compare_function=compare,
            source_file=logfile,
            logic_inconsistency_trace_file='logs/memgraph_logic_error.tsv',
            database_name='memgraph',
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
    scheduler(config.get('memgraph', 'input_path'), MemgraphTester(f"memgraph_misc"), "memgraph")


if __name__ == "__main__":
    if config.get('GLOBAL', 'env') == "debug":
        Tester = MemgraphTester('dev_graph')
        Tester.single_file_testing("query_file/database0-cur.log")
    else:
        schedule()
