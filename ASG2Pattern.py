import random
from Pattern2ASG import TransformPattern2ASG

def traversal(G, u_id, depth):
    res = G.Nodes[u_id].content
    Availiable_edges = list()
    for edge in G.Nodes[u_id].edges:
        if edge["id"] not in G.DeletedEdge: 
            Availiable_edges.append(edge)
    length = len(Availiable_edges)
    # print(len(G.Nodes[u_id].edges))
    if length == 0: 
        G.DeletedNode.add(u_id)
        return res
    
    if depth > 0 and random.randint(0, length) == 0:
        return res
    if depth == 0 and random.randint(0, length * 3) == 0:
        return res 

    go = random.choice(Availiable_edges)
    res = res + go["content"]
    G.DeletedEdge.add(go["id"])
    res = res + traversal(G, go["v"], depth + 1)
    if length == 1:
        G.DeletedNode.add(u_id)
    return res

def TransformASG2Pattern(G):
    result = []
    while len(G.DeletedEdge) < G.M and len(G.DeletedNode) < G.N:
        Availiable_Nodes = list()
        for i in range(0, G.N):
            if i not in G.DeletedNode: 
                Availiable_Nodes.append(i)
        start_id = random.choice(Availiable_Nodes)
        result.append(traversal(G, start_id, 0))
    result = ", ".join(result)
    # print(result)
    return result
    

if __name__ == "__main__":
    G = TransformPattern2ASG("(n0 :L3 :L6)<-[r0 :T0]-(n1)-[r1 :T3]->(n2 :L6 :L2 :L1), (n3 :L0)-[r2 :T0]->(n4 :L6)<-[r3 :T2]-(n5 :L1), (n3 :L0)<-[r4 :T0]-(n6 :L6 :L0)<-[r5 :T2]-(n7 :L4)")
    TransformASG2Pattern(G)
