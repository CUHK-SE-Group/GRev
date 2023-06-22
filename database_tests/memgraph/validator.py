import csv

import TestMemGraph
import configs


def read_logic_error_file():
    with open('logs/memgraph_logic_error.tsv', mode='r') as file:
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
            result1, _ = client.run(query1)
            result2, _ = client.run(query2)
            # print("result1: ", result1)
            # print("result2: ", result2)
            eq = TestMemGraph.compare(result1, result2)
            print("eq or not: ", eq)
            print("\n=============\n")
        except Exception as e:
            print(e)
    return None


if __name__ == "__main__":
    read_logic_error_file()
