import time
from cypher.ngql.query_generator import *
from gdb_clients.nebula import Nebula


def test_nebula_simple():
    t = time.time()
    log_file = f"./query_producer/cypher/{t}.log"
    qg = QueryGenerator(log_file)
    with open(log_file, 'r') as f:
        create_statements = f.read()
        f.close()
    create_statements = create_statements.split("\n")

    nb = Nebula()
    nb.clear()
    nb.batch_run(create_statements)

    nb.run("CREATE(n0:L2 {id : 8});")
    print(nb.run("MATCH (n)"))

    match_statements = [qg.gen_query() for _ in range(10)]
    for query_a, query_b in match_statements:
        print(f"query_a = {query_a}")
        res_a, res_b = nb.run(query_a), nb.run(query_b)
        assert res_a, res_b
        print(res_a)
