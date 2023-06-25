from abc import ABC, abstractmethod


class Node:
    def __init__(self, idx, name, labels, properties):
        """Watch out for nodes with empty names"""
        self.idx = idx
        self.name = name
        """The sets of label expressions and property key-value expressions"""
        self.labels = labels
        self.properties = properties
        """The list of incident edges"""
        self.edges = []

    def add_edge(self, target_node_idx, content, edge_idx):
        edge = {"v": target_node_idx,
                "content": content,
                "id": edge_idx
                }
        self.edges.append(edge)


class ASG:
    def __init__(self):
        self.num_nodes = 0
        self.num_edges = 0
        self.nodes = []
        self.deleted_nodes = set()
        self.deleted_edges = set()

    def add_node(self, node):
        self.nodes.append(node)
        self.num_nodes += 1

    def add_edge(self, v1_idx, v2_idx, edge_content):
        edge_content = edge_content.strip(" ")
        edge_idx = self.num_edges
        self.nodes[v1_idx].add_edge(v2_idx, edge_content, edge_idx)
        if edge_content.startswith("<"):
            edge_content = edge_content[1:] + ">"
        elif edge_content.endswith(">"):
            edge_content = "<" + edge_content[:-1]
        self.nodes[v2_idx].add_edge(v1_idx, edge_content, edge_idx)
        self.num_edges += 1


class AbstractASGOperator(ABC):
    @abstractmethod
    def asg2pattern(self, asg: ASG):
        pass

    @abstractmethod
    def pattern2asg(self, pattern: str):
        pass