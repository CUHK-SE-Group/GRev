from gdb_clients.redis_graph import Redis
from reproduce.test_helper import run_test_from_file


if __name__ == "__main__":
    client = Redis(uri="localhost", database="validate")

    # 3081
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/redis/redis_3081.log",
                       query_statements=[
                            f"MATCH (n0 :L2)<-[r0 :T2]-(n1 :L2), (n3 :L4)-[r2 :T0]->(n4 :L4) OPTIONAL MATCH (n9 :L2)-[r7 :T4]->(n10 :L0), (n12 :L2)-[r9 :T3]->(n4)<-[r8 :T3]-(n11 :L2) WHERE (r8.id) <> (r9.id) RETURN (r8.k51) AS a1",
                            f"MATCH (n0 :L2)<-[r0 :T2]-(n1 :L2), (n3 :L4)-[r2 :T0]->(n4 :L4) OPTIONAL MATCH (n9 :L2)-[r7 :T4]->(n10 :L0), (n11 :L2)-[r8 :T3]->(n4)<-[r9 :T3]-(n12 :L2) WHERE (r8.id) <> (r9.id) RETURN (r8.k51) AS a1"
                        ], message="Running Redis-3081:")

    # 3091
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/redis/redis_3091.log",
                       query_statements=[
                           f"MATCH (n0:L5)-[r0:T5]->(n1:L0:L1)<-[r1:T5]-(n2:L3:L4:L1), (n3:L5:L4)-[r2:T4]->(n4:L3:L2)-[r3:T4]->(n5:L2:L5:L4), (n6)<-[r4:T0]-(n7:L1)<-[r5:T3]-(n8:L2) WITH n8 OPTIONAL MATCH (n7:L1)-[r7:T1]->(n10), (n2)<-[r9:T1]-(n12) RETURN n7.id",
                           f"MATCH (n0:L5)-[r0:T5]->(n1:L0:L1)<-[r1:T5]-(n2:L3:L4:L1), (n3:L5:L4)-[r2:T4]->(n4:L3:L2)-[r3:T4]->(n5:L2:L5:L4), (n6)<-[r4:T0]-(n7:L1)<-[r5:T3]-(n8:L2) WITH n8 OPTIONAL MATCH (n7:L1)-[r7:T1]->(n10), (n2)<-[r9:T1]-(n12) WHERE n7.id = 117 RETURN n7.id",
                           f"MATCH (n0:L5)-[r0:T5]->(n1:L0:L1)<-[r1:T5]-(n2:L3:L4:L1), (n3:L5:L4)-[r2:T4]->(n4:L3:L2)-[r3:T4]->(n5:L2:L5:L4), (n6)<-[r4:T0]-(n7:L1)<-[r5:T3]-(n8:L2) WITH n8 OPTIONAL MATCH (n7:L1)-[r7:T1]->(n10), (n2)<-[r9:T1]-(n12) WHERE n7.id = 117 OR n7.id = 120 RETURN n7.id"
                       ], message="Running Redis-3091:")

    # 3091
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/redis/redis_3093.log",
                       query_statements=[
                           f"MATCH (n3)-[]->(n4 :L1), (n0)<-[]-(n3) MATCH (n0)<-[]-(n1 :L2)-[]->(n1 :L2) RETURN COUNT(*)",
                           f"MATCH (n0)<-[]-(n3)-[]->(n4 :L1) MATCH (n0)<-[]-(n1 :L2)-[]->(n1 :L2) RETURN COUNT(*)"
                       ], message="Running Redis-3093:")

    # 3100
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/redis/redis_3100.log",
                       query_statements=[
                           f"MATCH (n0 :L3 :L2), (n1 :L0) MATCH (n2 :L1)<-[r2 :T4]-(n3 :L3), (n0 :L3), (n0) WITH n2 MATCH (n4 :L3)<-[r3 :T3]-(n1), (n0) WHERE (n2.k7) RETURN COUNT(*)",
                           f"MATCH (n1 :L0), (n0 :L3 :L2) MATCH (n3 :L3)-[r2 :T4]->(n2 :L1), (n0 :L3) WITH n2 MATCH (n4 :L3)<-[r3 :T3]-(n1), (n0) WHERE (n2.k7) RETURN COUNT(*)"
                       ], message="Running Redis-3100:")

    # 3114
    run_test_from_file(client=client,
                       create_statements_file="./reproduce/redis/redis_3114.log",
                       query_statements=[
                           f"MATCH (n1 :L3)<-[r1 :T1]-(n2 :L4), (n3 :L0 :L1 :L4)<-[r2 :T2]-(n4 :L1 :L0)<-[r3 :T5]-(n5 :L3) WITH DISTINCT n4 MATCH (n3 :L4)<-[]-(n4 :L0)<-[]-(n5)  MATCH (n8 :L0)-[r6 :T5]->(n9), (n2 :L0)<-[r10 :T2]-(n12 :L1), (n11 :L3)-[r8 :T1]->(n3), (n10 :L3)-[r7 :T5]->(n9) RETURN n10.k20",
                           f"MATCH (n1 :L3)<-[r1 :T1]-(n2 :L4), (n3 :L0 :L1 :L4)<-[r2 :T2]-(n4 :L1 :L0)<-[r3 :T5]-(n5 :L3) WITH DISTINCT n4 MATCH (n3 :L4)<-[]-(n4 :L0)<-[]-(n5)  MATCH (n2 :L0)<-[r10 :T2]-(n12 :L1), (n11 :L3)-[r8 :T1]->(n3), (n10 :L3)-[r7 :T5]->(n9), (n8 :L0)-[r6 :T5]->(n9) RETURN n10.k20"
                       ], message="Running Redis-3114:")
