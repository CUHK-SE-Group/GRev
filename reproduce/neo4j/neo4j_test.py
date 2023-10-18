from gdb_clients.neo4j_db import Neo4j
from reproduce import test_helper


# WARNING: still work-in-progress


if __name__ == "__main__":
    uris = [
        "bolt://localhost:10200",
        "bolt://localhost:10201",
        "bolt://localhost:10202",
        "bolt://localhost:10203",
        "bolt://localhost:10204",
        "bolt://localhost:10205"
    ]
    q1 = f'MATCH (n1)-[r1 WHERE (r1.p18 <> r1.p16) AND (r1.p27 < r1.p7)]-(n2:(!L0|!L4)) RETURN *'
    for uri in uris:
        client = Neo4j(uri=uri, username="neo4j", passwd="testtest")
        print(f"Testing against database at {uri}")
        test_helper.run_test_from_file(client=client,
                                       create_statements_file='./reproduce/neo4j/create.log',
                                       query_statements=[q1])
