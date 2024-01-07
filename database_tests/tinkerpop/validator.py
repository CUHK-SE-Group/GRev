import csv
from gdb_clients import *
import configs
import re
import subprocess
import TestTinkerpop
from configs import config

def read_logic_error_file():
    with open('logs/thinkerpop_logic_error.tsv', mode='r') as file:
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
    client = Tinkerpop()
    if config.get('tinkerpop', 'input_mode') == "cypher":
        with open(log_file, 'r') as f:
            content = f.read()
            contents = content.strip().split('\n')
            create_statements = contents[4:-configs.query_len]
    else:
        with open(log_file, "r", encoding = "utf-8") as f:
            create_statements = f.read().strip().split('\n')
    client.clear()
    client.batch_run(create_statements)
          
    for query in query_pairs:
        result1 = client.run(query[0])
        result2 = client.run(query[1])
        if not TestTinkerpop.compare(result1, result2):
            print("inconsistency")
        print(result1)
        print(result2)
    return None
	



if __name__ == "__main__":
    validate("", "query_producer/logs/composite/database130-cur.log", [
        [
        "MATCH (n0 :L0 :L4)-[r0 :T3]->(n1 :L1)<-[r1 :T0]-(n2), (n4 :L0 :L3)<-[r3 :T1]-(n5 :L2)   RETURN COUNT(*)", 
        "MATCH (n1 :L1)<-[r0 :T3]-(n0 :L4 :L0), (n2)-[r1 :T0]->(n1 :L1), (n4 :L3 :L0), (n4 :L3 :L0)<-[r3 :T1]-(n5 :L2) RETURN COUNT(*)"]
        ])
