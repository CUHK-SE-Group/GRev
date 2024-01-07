from gdb_clients.neo4j_db import Neo4j
from reproduce import test_helper


# WARNING: still work-in-progress


if __name__ == "__main__":
    uris = [
        # "neo4j://localhost:10111",
        "neo4j://localhost:10201",
        "neo4j://localhost:10202",
        "neo4j://localhost:10204",
        "neo4j://localhost:10205"
    ]

    for uri in uris:
        client = Neo4j(uri=uri, username="neo4j", passwd="testtest")
        print(f"Testing against database at {uri}")

        test_helper.run_test_from_file(client=client,
                                       create_statements_file='./reproduce/neo4j/dummy.log',
                                       query_statements=[
                                            r'MATCH (en:Entity {EntityType:"Offer"}) <-[:E_EN]- (e:Event) -[df:DF]-> (e2:Event) -[:E_EN]-> (en2:Entity {EntityType:"Offer"}) WHERE df.EntityType = "Case_AWO" RETURN count(df)'
                                       ], message="Dummy")

        # Neo4j-13168
        # test_helper.run_test_from_file(client=client,
        #                                create_statements_file='./reproduce/neo4j/neo4j_13168.log',
        #                                query_statements=[
        #                                    r'MATCH (n1), (n1)<-[r2 :T3]-(n3 :L0) WITH (n3.k2) AS a1 MATCH (n0 :L1)-[]->(n1)<-[]-(n2 :L2) WHERE false WITH a1 ORDER BY a1 RETURN count(*)'
        #                                ], message="Testing Neo4j-13168")
        #
        # # Neo4j-13170
        # test_helper.run_test_from_file(client=client,
        #                                create_statements_file='./reproduce/neo4j/neo4j_13170.log',
        #                                query_statements=[
        #                                    r'MATCH (n0) MATCH (n1) MATCH (n2) MATCH (n3) MATCH (n4) MATCH (n5) MATCH (n6) MATCH (n7) MATCH (n8) RETURN COUNT(*)'
        #                                ], message="Testing Neo4j-13170")
        #
        # # Neo4j-13212
        # test_helper.run_test_from_file(client=client,
        #                                create_statements_file='./reproduce/neo4j/neo4j_13212.log',
        #                                query_statements=[
        #                                    r'MATCH (n0 :L2)<-[r0 :T6]-(n1 :L4 :L0)-[r1 :T1]->(n2), (n3 :L2 :L3 :L5)<-[r2 :T1]-(n4)  WITH (n1.k28) AS a0, r2, collect(-308332354) AS a1, (r1.k47) AS a2 UNWIND [1456128099, 1210199808] AS a3 UNWIND [1706326841, -1735775121, -1735775121] AS a4 MATCH (n6 :L5)<-[r4 :T5]-(n7 :L5), (n9 :L5)-[r6 :T6]->(n2)-[r7 :T2]->(n10), (n11 :L1)-[r8 :T5]->(n6)-[r9 :T3]->(n12 :L6 :L4) WHERE NOT true RETURN a3, a1, (n7.k35) AS a6 ORDER BY a3, a1, a6 DESC',
        #                                    r"MATCH (n0)-[r0 :T3]->(n1 :L6 :L3)<-[r1 :T3]-(n2 :L4), (n0)-[r2 :T4]->(n3) WITH * UNWIND [(n1.k18), 919424523] AS a0 MATCH (n4 :L5)<-[r3 :T0]-(n5 :L1 :L0 :L6)-[r4 :T5]->(n3) MATCH (n4 :L2)<-[]-(n5 :L1)-[]->(n3 :L2) WHERE (NOT true) OPTIONAL MATCH (n1)<-[]-(n0)-[]->(n3) WHERE (NOT (r4.k76)) WITH n3, n5, (r1.k63) AS a1, (n2.k28) AS a2 ORDER BY (n3.k15), (n5.k8), (n5.k37) WITH max('V') AS a3, n5 RETURN DISTINCT a3;"
        #                                ], message="Testing Neo4j-13212")
        #
        # # Neo4j-13229
        # # test_helper.run_test_from_file(client=client,
        # #                                create_statements_file='./reproduce/neo4j/neo4j_13229.log',
        # #                                query_statements=[
        # #                                    r'MATCH (A)<-[:(%)*1..2]-(B) RETURN *',
        # #                                    r'MATCH (A)<-[:%]-(B) RETURN *',
        # #                                    r'MATCH (A)<-[:(KNOWS)*1..2]-(B) RETURN *'
        # #                                ], message="Testing Neo4j-13229")
        #
        # # Neo4j-13262
        # # test_helper.run_test_from_file(client=client,
        # #                                create_statements_file='./reproduce/neo4j/neo4j_13262.log',
        # #                                query_statements=[
        # #                                    r'MATCH p=(v5 {} )-[*..2 {roles: "Sen. Kevin Keeley"}]-() RETURN p'
        # #                                ], message="Testing Neo4j-13262")
        #
        # # Neo4j-13234
        # test_helper.run_test_from_file(client=client,
        #                                create_statements_file='./reproduce/neo4j/neo4j_13234.log',
        #                                query_statements=[
        #                                    r'MATCH (n1)-[r1 WHERE (r1.p18 <> r1.p16) AND (r1.p27 < r1.p7)]-(n2:(!L0|!L4)) RETURN *'
        #                                ], message="Testing Neo4j-13234")
