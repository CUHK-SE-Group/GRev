import json

if __name__ == "__main__":
    with open("./mutator/gremlin/schemas/query-01.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
    with open("./mutator/gremlin/schemas/query-01.log", "w", encoding = "utf-8") as g:
        for d in data:
            print("Query1: " + d["Query1"], file = g)
            print("Query2: " + d["Query2"], file = g)
            print("\n", file = g)