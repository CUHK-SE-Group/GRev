from abc import ABC, abstractmethod


class Node:
    def __init__(self, _id, _name, _labels):
        self.id, self.name = _id, _name
        self.labels, self.edges = _labels, []
        self.content = "(" + self.name
        if type(self.labels) == type(set()):
            for label in self.labels:
                self.content += " :" + label
        self.content = self.content + ")"

    def AddEdge(self, target_node_id, content, edge_id):
        edge = {"v": target_node_id,
                "content": content,
                "id": edge_id
                }
        self.edges.append(edge)


class ASG:
    def __init__(self):
        self.N, self.M, self.Nodes = 0, 0, []
        self.DeletedEdge, self.DeletedNode = set(), set()

    # def __eq__(self, other):
    #     if self.N == other.N \
    #             and self.M == other.M \
    #             and self.Nodes == other.Nodes \
    #             and self.DeletedEdge == other.DeletedEdge \
    #             and self.DeletedNode == other.DeletedNode:
    #         return True
    #     return False

    def AddNode(self, _node):
        self.Nodes.append(_node)
        self.N += 1

    def AddEdge(self, v1_id, v2_id, edge_content):
        edge_content = edge_content.strip(" ")
        self.Nodes[v1_id].AddEdge(v2_id, edge_content, self.M)
        if edge_content.startswith("<"):
            edge_content = edge_content[1:] + ">"
        elif edge_content.endswith(">"):
            edge_content = "<" + edge_content[:-1]
        self.Nodes[v2_id].AddEdge(v1_id, edge_content, self.M)
        self.M += 1


class AbstractASGOperator(ABC):
    @abstractmethod
    def asg2pattern(self, asg: ASG):
        pass

    @abstractmethod
    def pattern2asg(self, pattern: str):
        pass