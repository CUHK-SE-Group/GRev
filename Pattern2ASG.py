from ASGschema import *

def Pattern2List(pattern):
    patterns, result = pattern.split(","), []
    for pattern in patterns:
        pattern = pattern.strip(" ")
        pattern = pattern.strip("\n")
        v1, r, v2 = "", "", ""
        for i in range(0, len(pattern)):
            if not(v1.endswith(")")):
                v1 = v1 + pattern[i]
            elif pattern[i] == "(" or v2 != "":
                v2 = v2 + pattern[i]
                if pattern[i] == ")":
                    result.append((v1, r, v2))
                    v1, r, v2 = v2, "", ""
            else: r = r + pattern[i]
    # print(result)
    return result

def Pattern2Node(pattern):
    pattern = pattern.strip(" " ).strip(")").strip("(")
    patterns = pattern.split(":")
    result = {"name": patterns[0].strip(" ")}
    labels = set()
    for i in range(1, len(patterns)):
        labels.add(patterns[i].strip(" "))
    result["labels"] = labels
    return result


def TransformPattern2ASG(pattern):
    G = ASG()
    Node2Labels, Node2Id, Id_index = dict(), dict(), 0
    patterns = Pattern2List(pattern)
    for edge in patterns:
        v1, v2 = edge[0], edge[2]
        r1, r2 = Pattern2Node(v1), Pattern2Node(v2)
        for r in r1, r2:
            name, labels = r["name"], r["labels"]
            if name not in Node2Labels.keys():
                Node2Labels[name] = "ALL"
                Node2Id[name] = Id_index
                Id_index += 1
            if len(labels) > 0:
                if Node2Labels[name] == "ALL": 
                    Node2Labels[name] = labels
                else: Node2Labels[name] = Node2Labels[name] & labels

    for name in sorted(Node2Labels.keys(), key = lambda x : Node2Id[x]):
        labels, Id = Node2Labels[name], Node2Id[name]
        G.AddNode(Node(Id, name, labels))
    
    for edge in patterns:
        v1, v2 = edge[0], edge[2]
        r1, r2 = Pattern2Node(v1), Pattern2Node(v2)
        # print(r1["name"], r2["name"])
        G.AddEdge(Node2Id[r1["name"]], Node2Id[r2["name"]], edge[1])
        
    return G

        



if __name__ == "__main__":
    TransformPattern2ASG("(n0 :L3 :L6)<-[r0 :T0]-(n1)-[r1 :T3]->(n2 :L6 :L2 :L1), (n3 :L0)-[r2 :T0]->(n4 :L6)<-[r3 :T2]-(n5 :L1), (n3 :L0)<-[r4 :T0]-(n6 :L6 :L0)<-[r5 :T2]-(n7 :L4)")
