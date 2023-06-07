import csv
from gdb_clients import *
import configs
import re
import subprocess

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
    with open(log_file, 'r') as f:
        content = f.read()
        contents = content.strip().split('\n')
        create_statements = contents[4:-configs.query_len]
        client.clear()
        client.batch_run(create_statements)
    for query in query_pairs:
        pattern = r':L\d+'
        q1 = re.sub(pattern, '', query[0])
        result = subprocess.check_output(["java", "-jar", "./query_producer/Cypher.jar", q1], universal_newlines=True)
        q2 = re.sub(pattern, '', query[1])
        result = subprocess.check_output(["java", "-jar", "./query_producer/Cypher.jar", q2], universal_newlines=True)
        print(result)
    return None


if __name__ == "__main__":
    read_logic_error_file()
