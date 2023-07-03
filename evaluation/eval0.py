from gdb_clients.redis_graph import Redis
from mutator.redis.query_transformer import QueryTransformer
import random


def count_number_of_plans_single(data_file, num_mutations=100, num_queries_generated=20):
    with open(data_file, 'r') as f:
        stuff = f.read()
    stuff = stuff.strip().split('\n')
    create_statements = stuff[4:-num_queries_generated]
    query_statements = stuff[-num_queries_generated:]

    database_name = "eval0_graph"
    r = Redis("10.20.10.27", database_name)
    r.batch_run(create_statements)

    base_query = max(query_statements, key=len)
    # base_query = random.choice(match_statements)
    cur_query = base_query
    qt = QueryTransformer()
    plans = set()
    for _ in range(num_mutations):
        plans.add(r.get_plan(cur_query))
        cur_query = qt.mutant_query_generator(cur_query)
    return len(plans)


def count_number_of_plans(num_cases=10, num_mutations=100, num_queries_generated=20):
    num_total = 0
    for idx in range(num_cases):
        data_file = f'./query_producer/logs/composite/database{idx}-cur.log'
        num = count_number_of_plans_single(data_file, num_mutations=num_mutations,
                                           num_queries_generated=num_queries_generated)
        print(f'Index = {idx}, result = {num}')
        num_total += num
    result = num_total / num_cases
    return result


if __name__ == '__main__':
    print(f'average = {count_number_of_plans(num_cases=50, num_queries_generated=10)}')
