from gdb_clients.redis_graph import Redis
from mutator.redis.query_transformer import QueryTransformer
import random
from configs import config

def count_number_of_plans_single(data_file, sample_method=random.choice, num_mutations=100, num_queries_generated=20):
    with open(data_file, 'r') as f:
        stuff = f.read()
    stuff = stuff.strip().split('\n')
    create_statements = stuff[4:-num_queries_generated]
    query_statements = stuff[-num_queries_generated:]

    database_name = "eval0_graph"
    r = Redis(config.get("redis", "uri"), database_name)
    r.batch_run(create_statements)

    num_take = 10
    step = 15

    base_queries = sample_method(query_statements, num_take)
    qt = QueryTransformer()

    num_queries = []
    num_plans = []
    for k in range(num_mutations+1):
        if k % step == 0:
            num_queries.append(0)
            num_plans.append(0)

    for base_query in base_queries:
        queries = set()
        plans = set()
        p = 0
        cur_query = base_query
        for k in range(num_mutations+1):
            queries.add(cur_query)
            plans.add(r.get_plan(cur_query))
            if k % step == 0:
                num_queries[p] += len(queries)
                num_plans[p] += len(plans)
                p += 1
            cur_query = qt.mutant_query_generator(cur_query)

    return num_queries, num_plans


def count_number_of_plans(num_cases=10, num_mutations=300, num_queries_generated=20, sample_method=random.choice):
    num_queries, num_plans = [], []
    for idx in range(num_cases):
        data_file = f'./query_producer/logs/composite/database{idx}-cur.log'
        with open("./evaluation/eval0.log", 'w+') as f:
            print(f'file = {data_file}')
            print(f'file = {data_file}', file=f)
        cur_num_queries, cur_num_plans = count_number_of_plans_single(data_file=data_file, sample_method=sample_method,
                                            num_mutations=num_mutations,
                                           num_queries_generated=num_queries_generated)
        if len(num_queries) < len(cur_num_queries):
            assert len(num_queries) == len(num_plans) == 0
            num_queries = [0] * len(cur_num_queries)
            num_plans = [0] * len(cur_num_plans)

        for k in range(len(cur_num_queries)):
            num_queries[k] += cur_num_queries[k]
            num_plans[k] += cur_num_plans[k]

    for k in range(len(num_queries)):
        num_queries[k] /= num_cases
        num_plans[k] /= num_cases

    return num_queries, num_plans


if __name__ == '__main__':
    def sample_largest(a, sz):
        assert len(a) >= sz
        a = sorted(a, key=len, reverse=True)
        return a[:sz]

    def sample_random(a, sz):
        assert len(a) >= sz
        return random.sample(a, sz)

    q1, p1 = count_number_of_plans(num_cases=50, num_mutations=300, num_queries_generated=5000,
                                   sample_method=sample_random)
    q2, p2 = count_number_of_plans(num_cases=50, num_mutations=300, num_queries_generated=5000,
                                   sample_method=sample_largest)

    with open("./evaluation/eval_real_queries.res", mode="w") as f:
        print(q1, file=f)
        print(p1, file=f)
        print(q2, file=f)
        print(p2, file=f)
