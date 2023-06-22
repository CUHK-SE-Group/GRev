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

        # 逐行读取数据
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
        pattern = r':L\d+'
        q1 = re.sub(pattern, '', query[0])
        q2 = re.sub(pattern, '', query[1])
        result1 = client.run(q1)
        result2 = client.run(q2)
        if not TestTinkerpop.compare(result1, result2):
            print("inconsistency")
        print(result1)
        print(result2)
    return None


if __name__ == "__main__":
    validate("", "query_producer/logs/composite/database10-cur.log", [
        [
        "MATCH (n2 ), (n3)<-[r2]-(n0) WHERE ((r2.id) > -1) OPTIONAL MATCH (n0)-[]->(n1)<-[]-(n2), (n2)<-[r3]-(n4) WHERE ((r3.k73) <= (n2.k4)) OPTIONAL MATCH (n3)<-[]-(n0)-[]->(n1) RETURN (r3.k69) AS a0, (n3.k12) AS a1;", 
        "MATCH (n0)-[r2]->(n3), (n2) WHERE ((r2.id) > -1) OPTIONAL MATCH (n2)<-[r3]-(n4), (n0)-[]->(n1)<-[]-(n2) WHERE ((r3.k73) <= (n2.k4)) OPTIONAL MATCH (n1)<-[]-(n0), (n3)<-[]-(n0) RETURN (r3.k69) AS a0, (n3.k12) AS a1;"]
        ])
