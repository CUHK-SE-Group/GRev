from gdb_clients.mem_graph import MemGraph
from reproduce.test_helper import run_test_from_file


if __name__ == "__main__":
    client = MemGraph()

    # 948
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/memgraph/memgraph_948.log",
                       query_statements=[
                           f"MATCH (n0 :L3)<-[r0 :T1]-(n1) WHERE (n0.k24) OPTIONAL MATCH (n2 :L2)<-[]-(n1 :L1), (n1 :L1)-[]->(n0) WITH * MATCH (n0)<-[]-(n1)-[]->(n2) RETURN *",
                           f"MATCH (n0 :L3)<-[r0 :T1]-(n1) WHERE (n0.k24) OPTIONAL MATCH (n0)<-[]-(n1 :L1)-[]->(n2 :L2) WITH * MATCH (n0)<-[]-(n1)-[]->(n2) RETURN *",
                           f"MATCH (n0 :L3)<-[r0 :T1]-(n1) WHERE (n0.k24) OPTIONAL MATCH (n2 :L2)<-[]-(n1 :L1), (n1 :L1)-[]->(n0) RETURN *",
                           f"MATCH (n0 :L3)<-[r0 :T1]-(n1) WHERE (n0.k24) OPTIONAL MATCH (n0)<-[]-(n1 :L1)-[]->(n2 :L2) RETURN *"
                       ], message="Running Memgraph-948:")

    # 954
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/memgraph/memgraph_954.log",
                       query_statements=[
                           f"MATCH (n0) WITH collect(n0) AS a0 WITH * MATCH (n1) RETURN * ORDER BY a0",
                           f"MATCH (n0) WITH collect(n0) AS a0 WITH * RETURN * ORDER BY a0"
                       ], message="Running Memgraph-954:")

    #1068
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/memgraph/memgraph_1068.log",
                       query_statements=[
                           f"MATCH (n1:L6)-[r1]->(n2:L5), (n3:L7)-[]->(n4)<-[r2]-(n5:L5), (n6:L1:L4)-[:T1 *..3]-(n7:L2:L7), (n5:L6) RETURN COUNT(*)",
                           f"MATCH (n2:L5)<-[r1]-(n1:L6), (n4)<-[r2]-(n5:L5:L6), (n3), (n3:L7)-[]->(n4), (n7:L2:L7)-[:T1 *..3]-(n6:L1:L4) RETURN COUNT(*)"
                       ], message="Running Memgraph-1068:")
