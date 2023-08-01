import csv
from configs.conf import config

import configs
from gdb_clients import *

def read_logic_error_file():
    with open('logs/neo4j_logic_error.tsv', mode='r') as file:
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
    client = Neo4j(config.get("neo4j", "uri"), config.get('neo4j', 'username'), config.get('neo4j', 'passwd'),'testtest')
    with open(log_file, 'r') as f:
        content = f.read()
        contents = content.strip().split('\n')
        create_statements = contents
        client.clear()
        client.batch_run(create_statements)
        res = client.run("MATCH (n0 :L1), (n5) MATCH (n6 :L0)<-[r4 :T5]-(n2), (n8 :L4)-[r7 :T6]->(n9 :L3 :L2) WHERE ((true AND (n9.k16)) AND ((r4.id) <> (r7.id))) WITH (r4.k74) AS a0, n5, r7 OPTIONAL MATCH (n0)<-[]-(n1)-[]->(n2), (n10 :L5 :L3)-[r8 :T3]->(n11) WHERE (n10.k22) RETURN (r7.k80) AS a1, a0, (r7.k81) AS a2")
        print(res)
    return None


if __name__ == "__main__":
    validate("", "./query_producer/cypher/1688330152.2368863.log", "")
