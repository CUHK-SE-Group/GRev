import csv

import TestRedis
import configs
from database_tests.reduce_module.simplify_query import eliminate_useless_clauses
from gdb_clients import Redis
from typing import List
# import pandas as pd
import time

import re

def read_logic_error_file():
    with open('logs/redis_logic_error.tsv', mode='r') as file:
        reader = csv.reader(file, delimiter='\t')

        # cluster the query with file name
        data = []
        for row in reader:
            if len(data) == 0 or data[-1][1] == row[1]:
                data.append(row)
            else:
                r = validate(data[0][0], data[0][1], [(i[2], i[3]) for i in data])
                data = [row]
        r = validate(data[0][0], data[0][1], [(i[2], i[3]) for i in data])


def validate(database, log_file, query_pairs):
    if "203" not in log_file:
        return
    client = Redis("10.20.10.27", database + "_validation")
    with open(log_file, 'r') as f:
        content = f.read()
        contents = content.strip().split('\n')
        create_statements = contents[4:-configs.query_len]
        client.clear()
        client.batch_run(create_statements)

    dfs = []
    for query1, query2 in query_pairs:
        try:
            reduce(client, query1, query2)
        except Exception as e:
            print(e)
        # print(query1)
        # print(query2)
        continue
    return dfs


def compare(array1: List[list], array2: List[list]):
    sorted_arr1, sorted_arr2 = [], []
    for i in array1:
        i.sort(key=lambda x: x.__str__())
        sorted_arr1.append(i.__str__())
    for i in array2:
        i.sort(key=lambda x: x.__str__())
        sorted_arr2.append(i.__str__())
    dict1, dict2 = {}, {}
    for i in sorted_arr1:
        if i in dict1:
            dict1[i] += 1
        else:
            dict1[i] = 1
    for i in sorted_arr2:
        if i in dict2:
            dict2[i] += 1
        else:
            dict2[i] = 1
    compare_result1, compare_result2 = {}, {}
    for key, value in dict1.items():
        if key in dict2:
            if dict2[key] != value:
                compare_result1[key] = value
                compare_result2[key] = dict2[key]
        else:
            compare_result1[key] = value
    for key, value in dict2.items():
        if key not in dict1:
            compare_result2[key] = value

    # cnt1 = sum([v for _, v in compare_result1.items()])
    # cnt2 = sum([v for _, v in compare_result2.items()])
    # if cnt1 != cnt2:
    #     print("数量不符")

    if compare_result1 == {} and compare_result2 == {}:
        return True, compare_result1, compare_result2
    # df = pd.DataFrame([compare_result1, compare_result2])
    # ts = int(time.time() * 1000)
    # df.to_csv(f'data/dataframe_{ts}.csv', index=False)
    return False, compare_result1, compare_result2


def get_inverse_intervals(string, intervals):
    inverse_intervals = []
    string_length = len(string)
    if len(intervals) == 0:
        inverse_intervals.append([0, string_length - 1])
    else:
        start = 0
        for interval in intervals:
            end = interval[0] - 1
            if start <= end:
                inverse_intervals.append([start, end])
            start = interval[1] + 1
        if start <= string_length - 1:
            inverse_intervals.append([start, string_length - 1])
    return inverse_intervals


def simplify_expression(expression):
    stack = []
    result = ""
    for char in expression:
        if char == "(":
            stack.append(result)
            result = ""
        elif char == ")":
            if stack:
                result = stack.pop() + "(" + result + ")"
        else:
            result += char
    return result


def find_keywords(string, keywords):
    results = []
    for keyword in keywords:
        pattern = re.compile(keyword)
        matches = pattern.finditer(string)
        for match in matches:
            results.append([match.start(), match.end() - 1])
    results.sort()
    return results


def reduce(client, query1: str, query2: str):
    query1_res, _ = client.run(query1)
    query2_res, _ = client.run(query2)
    # 如果两个结果相等，则说明没有不一致的现象
    eq, compare_result1, compare_result2 = compare(query1_res, query2_res)
    if eq:
        return

    sum1 = sum([v for _,v in compare_result1.items()])
    sum2 = sum([v for _,v in compare_result2.items()])
    if sum1 == sum2:
        if sum1>2000:
            return
        print(compare_result1)
        print(compare_result2)
        keys1 = set([i for i, _ in compare_result1.items()])
        keys2 = set([i for i, _ in compare_result2.items()])
        if keys1 == keys2:
            print("数量总和一致, 且key一致")
        else:
            print("数量总和一致, 且key不一致")
        return
    print(compare_result1)
    print(compare_result2)
    keys1 = set([i for i, _ in compare_result1.items()])
    keys2 = set([i for i, _ in compare_result2.items()])
    if keys1 == keys2:
        print("数量总和不一致, 且key一致")
    else:
        print("数量总和不一致, 且key不一致")


if __name__ == "__main__":
    read_logic_error_file()
