from database_tests.helper import *
from database_tests.redis.TestRedis import RedisTester
# from mutator.redis.query_transformer import QueryTransformer
from mutator.query_transformer import QueryTransformer
import subprocess


def detect_number_of_bug_triggering_single(data_file, log_file='./evaluation/eval1.log',
                                           num_mutations=5000, num_queries_generated=20):
    with open(data_file, 'r') as f:
        stuff = f.read()
    stuff = stuff.strip().split('\n')
    create_statements = stuff[4:-num_queries_generated]
    base_queries = stuff[-num_queries_generated:]

    assert (len(base_queries) == num_queries_generated)

    database_name = "eval1_graph"
    rt = RedisTester(database_name)
    num_total = rt.single_file_testing_alt(logfile=data_file, create_statements=create_statements,
                                           query_statements=base_queries)

    with open(log_file, 'w+') as f:
        print(f'file = {data_file}, result = {num_total}', file=f)

    return num_total


def detect_number_of_bug_triggering(num_cases=10, num_mutations=5000, num_queries_generated=20):
    num_total = 0
    for idx in range(num_cases):
        print(f'Case #{idx}')
        data_file = f'./query_producer/logs/composite/database{idx}-cur.log'
        num_total += detect_number_of_bug_triggering_single(data_file, num_mutations=num_mutations,
                                                            num_queries_generated=num_queries_generated)
    return num_total


if __name__ == '__main__':
    num_cases = 50
    num_queries_generated = 5000

    # stuff = [
    #     "java",
    #     "-jar",
    #     "GDsmith.jar",
    #     "--num-tries",
    #     f'{num_cases}',
    #     "--num-queries",
    #     f'{num_queries_generated}',
    #     "--algorithm",
    #     "compared3",
    #     "--num-threads",
    #     "2",
    #     "composite"
    # ]
    # subprocess.run(stuff, cwd="./query_producer")

    result = detect_number_of_bug_triggering(num_cases=num_cases, num_mutations=5,
                                             num_queries_generated=num_queries_generated)
    print(f'final_result = {result}')
