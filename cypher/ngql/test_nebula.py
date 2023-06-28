from gdb_clients.nebula import *
from cypher.ngql.query_generator import *


def test_nebula():
    nb = Nebula("session_pool_test")
    qg = QueryGenerator()
    for _ in range(10):
        qa, qb = qg.gen_query()
        assert nb.run(qa) == nb.run(qb)

test_nebula()