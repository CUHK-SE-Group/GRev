from database_tests.helper import *
from database_tests.redis.TestRedis import RedisTester
from mutator.redis.query_transformer import QueryTransformer


def detect_number_of_bug_triggering_single(data_file, num_mutations=5000, num_queries_generated=20):
    with open(data_file, 'r') as f:
        stuff = f.read()
    stuff = stuff.strip().split('\n')
    create_statements = stuff[4:-num_queries_generated]
    query_statements = stuff[-num_queries_generated:]

    database_name = "eval1_graph"
    rt = RedisTester(database_name)

    qt = QueryTransformer()
    for i in range(num_queries_generated):
        base_query = query_statements[i]
        match_statements = [(base_query, qt.mutant_query_generator(base_query)) for _ in range(num_mutations)]
        rt.single_file_testing_alt(logfile=data_file, create_statements=create_statements,
                                   match_statements=match_statements)


def detect_number_of_bug_triggering(num_cases=10, num_mutations=5000, num_queries_generated=20):
    num_total = 0
    for idx in range(num_cases):
        print(f'Case #{idx}')
        data_file = f'./query_producer/logs/composite/database{idx}-cur.log'
        detect_number_of_bug_triggering_single(data_file, num_mutations=num_mutations,
                                           num_queries_generated=num_queries_generated)
    result = num_total / num_cases
    return result


if __name__ == '__main__':
    detect_number_of_bug_triggering(num_cases=10, num_mutations=100, num_queries_generated=100)
