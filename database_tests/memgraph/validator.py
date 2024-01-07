import csv

import TestMemGraph
import configs


def read_logic_error_file():
    with open('logs/memgraph_logic_error.tsv', mode='r') as file:
        reader = csv.reader(file, delimiter='\t')

        data = []
        for row in reader:
            if len(data) == 0 or data[-1][1] == row[1]:
                data.append(row)
            else:
                validate(data[0][0], data[0][1], [(i[2], i[3]) for i in data])
                data = [row]
        validate(data[0][0], data[0][1], [(i[2], i[3]) for i in data])


def validate(database, log_file, query_pairs):
    client = TestMemGraph.MemGraph()
    with open(log_file, 'r') as f:
        content = f.read()
        contents = content.strip().split('\n')
        create_statements = contents[4:-configs.query_len]
        client.clear()
        client.batch_run(create_statements)

    for query1, query2 in query_pairs:
        print("query1: " + query1)
        print("query2: " + query2)

        try:
            result1, t1 = client.run(query1)
            result2, t2 = client.run(query2)
            # print("result1: ", result1)
            # print("result2: ", result2)
            eq = TestMemGraph.compare(result1, result2)
            print("eq or not: ", eq)
            print(t1, t2)
            print("\n=============\n")
        except Exception as e:
            print(e)
    return None


if __name__ == "__main__":
    validate("d", "/home/nn/pattern-transformer/query_producer/logs/composite/database100-cur.log",  [("MATCH (n0)-[r0 :T0]->(n1)-[r1 :T3]->(n2 :L0), (n4 :L4) WHERE (((r0.id) > -1) AND ((r0.id) <> (r1.id))) WITH max('cj') AS a0, r0, n4, r1 ORDER BY (r0.k35), (n4.k23), (r1.k51) DESC WHERE (NOT (r0.k34)) WITH (n4.k26) AS a1, a0, r1 WITH * WHERE (false OR true) OPTIONAL MATCH (n6), (n4)-[r6 :T5]->(n8) WHERE ((r6.k66) CONTAINS (r6.k66)) WITH n8, n6, r1 OPTIONAL MATCH (n3)<-[]-(n4 :L4)-[]->(n5) RETURN 0 AS a2;",
    "MATCH (n0)-[r0 :T0]->(n1), (n2 :L0), (n1)-[r1 :T3]->(n2 :L0), (n4 :L4) WHERE (((r0.id) > -1) AND ((r0.id) <> (r1.id))) WITH max('cj') AS a0, r0, n4, r1 ORDER BY (r0.k35), (n4.k23), (r1.k51) DESC WHERE (NOT (r0.k34)) WITH (n4.k26) AS a1, a0, r1 WITH * WHERE (false OR true) OPTIONAL MATCH (n6), (n8)<-[r6 :T5]-(n4) WHERE ((r6.k66) CONTAINS (r6.k66)) WITH n8, n6, r1 OPTIONAL MATCH (n5)<-[]-(n4 :L4)-[]->(n3) RETURN 0 AS a2;"                                                                          
    )])
