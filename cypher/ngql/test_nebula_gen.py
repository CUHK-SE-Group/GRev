from cypher.ngql.query_generator import *
import gdb_clients.nebula


def test_nebula_gen():
    qg = QueryGenerator()
    nb = gdb_clients.nebula.Nebula()
    for _ in range(10000):
        qa, qb = qg.gen_query()
        ra, rb = nb.run(qa), nb.run(qb)
        assert ra == rb
        print(f'Result = {ra}')
