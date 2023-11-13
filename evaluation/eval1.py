from database_tests.redis.TestRedis import RedisTester
from datetime import datetime


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
    num_logic, num_performance = rt.single_file_testing_alt(logfile=data_file, create_statements=create_statements,
                                           query_statements=base_queries)

    with open(log_file, mode='a') as f:
        print(f'current time: {datetime.now()}', file=f)
        print(f'file = {data_file}, #logic = {num_logic}, #performance = {num_performance}', file=f)
        print(file=f)

    return num_logic, num_performance


def detect_number_of_bug_triggering(num_cases=10, num_mutations=5000, num_queries_generated=20):
    total_num_logic, total_num_performance = 0, 0
    offset = 300
    for idx in range(num_cases):
        data_file = f'./query_producer/logs/composite/database{offset + idx}-cur.log'
        num_logic, num_performance = detect_number_of_bug_triggering_single(data_file, num_mutations=num_mutations,
                                                            num_queries_generated=num_queries_generated)
        total_num_logic += num_logic
        total_num_performance += num_performance

    return total_num_logic, total_num_performance


if __name__ == '__main__':
    num_cases = 300
    num_queries_generated = 5000

    with open("./evaluation/eval1.log", mode='a') as f:
        print(f'starting time: {datetime.now()}', file=f)
        print(file=f)

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

    total_num_logic, total_num_performance = detect_number_of_bug_triggering(num_cases=num_cases, num_mutations=5,
                                             num_queries_generated=num_queries_generated)

    with open("./evaluation/eval1.log", mode='a') as f:
        print(f'total #logic = {total_num_logic}, total #performance = {total_num_performance}', file=f)

    with open("./evaluation/eval1.log", mode='a') as f:
        print(f'finishing time: {datetime.now()}', file=f)
        print(file=f)
