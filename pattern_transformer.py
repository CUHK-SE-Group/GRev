import random
from config import logger
from schema import *


class PatternTransformer(AbstractASGOperator):
    def __traversal(self, G, u_id, depth):
        res = G.Nodes[u_id].content
        Availiable_edges = list()
        for edge in G.Nodes[u_id].edges:
            if edge["id"] not in G.DeletedEdge:
                Availiable_edges.append(edge)
        length = len(Availiable_edges)
        # logger.debug(len(G.Nodes[u_id].edges))
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
        res = res + self.__traversal(G, go["v"], depth + 1)
        if length == 1:
            G.DeletedNode.add(u_id)
        return res

    def __pattern2list(self, pattern):
        patterns, result, isolated_nodes = pattern.split(","), [], []
        for pattern in patterns:
            pattern = pattern.strip(" ")
            pattern = pattern.strip("\n")
            v1, r, v2 = "", "", ""
            edge_counter = 0
            for i in range(0, len(pattern)):
                if not (v1.endswith(")")):
                    v1 = v1 + pattern[i]
                elif pattern[i] == "(" or v2 != "":
                    v2 = v2 + pattern[i]
                    if pattern[i] == ")":
                        result.append((v1, r, v2))
                        v1, r, v2 = v2, "", ""
                        edge_counter += 1
                else:
                    r = r + pattern[i]
            if edge_counter == 0 and len(v1) > 0:
                isolated_nodes.append(v1)
        logger.debug(result)
        logger.debug(isolated_nodes)
        return result, isolated_nodes

    def __pattern2node(self, pattern):
        pattern = pattern.strip(" ").strip(")").strip("(")
        patterns = pattern.split(":")
        result = {"name": patterns[0].strip(" ")}
        labels = set()
        for i in range(1, len(patterns)):
            labels.add(patterns[i].strip(" "))
        result["labels"] = labels
        return result

    def pattern2asg(self, pattern: str):
        G = ASG()
        Node2Labels, Node2Id, Id_index = dict(), dict(), 0
        patterns, isolated_nodes = self.__pattern2list(pattern)
        for edge in patterns:
            v1, v2 = edge[0], edge[2]
            r1, r2 = self.__pattern2node(v1), self.__pattern2node(v2)
            for r in r1, r2:
                name, labels = r["name"], r["labels"]
                if name not in Node2Labels.keys():
                    Node2Labels[name] = "ALL"
                    Node2Id[name] = Id_index
                    Id_index += 1
                if len(labels) > 0:
                    if Node2Labels[name] == "ALL":
                        Node2Labels[name] = labels
                    else:
                        Node2Labels[name] = Node2Labels[name] & labels

        for node in isolated_nodes:
            logger.debug(node)
            r = self.__pattern2node(node)
            name, labels = r["name"], r["labels"]
            if name not in Node2Labels.keys():
                Node2Labels[name] = "ALL"
                Node2Id[name] = Id_index
                Id_index += 1
            if len(labels) > 0:
                if Node2Labels[name] == "ALL":
                    Node2Labels[name] = labels
                else:
                    Node2Labels[name] = Node2Labels[name] & labels

        for name in sorted(Node2Labels.keys(), key=lambda x: Node2Id[x]):
            labels, Id = Node2Labels[name], Node2Id[name]
            G.AddNode(Node(Id, name, labels))

        for edge in patterns:
            v1, v2 = edge[0], edge[2]
            r1, r2 = self.__pattern2node(v1), self.__pattern2node(v2)
            G.AddEdge(Node2Id[r1["name"]], Node2Id[r2["name"]], edge[1])

        return G

    def asg2pattern(self, asg: ASG):
        result = []
        while len(asg.DeletedEdge) < asg.M or len(asg.DeletedNode) < asg.N:
            Availiable_Nodes = list()
            for i in range(0, asg.N):
                if i not in asg.DeletedNode:
                    Availiable_Nodes.append(i)
            start_id = random.choice(Availiable_Nodes)
            result.append(self.__traversal(asg, start_id, 0))
        result = ", ".join(result)
        logger.debug(result)
        return result


