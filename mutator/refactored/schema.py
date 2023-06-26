"""Data models used"""
from abc import ABC, abstractmethod
from mutator.refactored.helpers import *


class Node:
    """Stores node attributes in ASGs"""
    def __init__(self, idx, var, labels, properties):
        self.var = var
        # The sets of label expressions and property key-value expressions
        self.labels = labels
        self.properties = properties
        # The list of incident edges
        self.edges = []

    def add_edge(self, dest_idx, content, edge_idx):
        """Spans an edge going from the current node"""
        edge = {"v": dest_idx, "content": content, "id": edge_idx}
        self.edges.append(edge)


class ASG:
    """Abstract Syntax Graph"""
    def __init__(self):
        self.num_nodes = 0
        self.num_edges = 0
        self.nodes = []
        self.deleted_nodes = set()
        self.deleted_edges = set()

    def add_node(self, node):
        """Appends an node"""
        self.nodes.append(node)
        self.num_nodes += 1

    def get_node(self, idx):
        assert 0 <= idx < self.num_nodes
        return self.nodes[idx]

    def add_edge(self, st_idx, en_idx, edge_content: str):
        """
        Spans an edge between st and en
        :param st_idx: index of node st
        :param en_idx: index of node en
        :param edge_content: a string representing the edge
        :return:
        """
        edge_content = edge_content.strip(" ")
        edge_idx = self.num_edges

        # Edge going from st to en
        self.nodes[st_idx].add_edge(en_idx, edge_content, edge_idx)

        # Edge going from en to st
        self.nodes[en_idx].add_edge(st_idx, flip_edge(edge_content), edge_idx)

        self.num_edges += 1


class AbstractASGOperator(ABC):
    """Operator for ASGs"""
    @abstractmethod
    def asg_to_pattern(self, asg: ASG):
        """Transforms the given ASG into a pattern (a string)"""

    @abstractmethod
    def pattern_to_asg(self, pattern: str):
        """Transforms the given pattern (a string) into an ASG"""
