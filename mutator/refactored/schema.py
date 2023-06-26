"""Data models used"""
from abc import ABC, abstractmethod
from mutator.refactored.helpers import *
import random


class Node:
    """Stores node attributes in ASGs"""
    def __init__(self, idx, var, labels, properties):
        self.idx = idx
        self.var = var
        # The sets of label expressions and property key-value expressions
        self.labels = labels
        self.properties = properties
        assert isinstance(labels, set)
        assert isinstance(properties, set)
        # The list of incident edges
        self.edges = []

    def get_comparable(self):
        return self.var, sorted(list(self.labels)), sorted(list(self.properties))

    def add_edge(self, dest_idx, content, edge_idx):
        """Spans an edge going from the current node"""
        edge = (dest_idx, content, edge_idx)
        self.edges.append(edge)

    def get_edges(self):
        return self.edges

    def get_name(self):
        return self.var

    def get_labels(self):
        return self.labels

    def get_properties(self):
        return self.properties


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
        """Returns the node corresponding to the given index"""
        assert 0 <= idx < self.num_nodes
        return self.nodes[idx]

    def get_available_nodes(self):
        """Returns a list of all available nodes"""
        return [i for i in range(self.num_nodes) if i not in self.deleted_nodes]

    def get_available_edges(self, start_idx):
        """Given a starting node, returns a list of all available incident edges"""
        edges = self.nodes[start_idx].get_edges()
        return [e for e in edges if e[2] not in self.deleted_edges]

    def get_node_name(self, idx):
        return self.nodes[idx].get_name()

    def get_node_labels(self, idx):
        return self.nodes[idx].get_labels()

    def get_node_properties(self, idx):
        return self.nodes[idx].get_properties()

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

    def is_empty(self):
        return len(self.deleted_edges) == self.num_edges and len(self.deleted_nodes) == self.num_nodes

    def get_num_nodes(self):
        return self.num_nodes

    def get_num_edges(self):
        return self.num_edges

    def traverse(self, cur_idx, depth=0):
        result = [cur_idx]
        adj = self.get_available_edges(cur_idx)

        num_choices = len(adj)
        if num_choices == 0:
            self.deleted_nodes.add(cur_idx)
            return result

        if depth > 0 and random.randint(0, num_choices) == 0:
            return result
        if depth == 0 and random.randint(0, 3*num_choices) == 0:
            return result

        if num_choices == 1:
            self.deleted_nodes.add(cur_idx)
        # Randomly picks an outgoing edge
        nxt_idx, edge_content, edge_idx = random.choice(adj)
        assert edge_idx not in self.deleted_edges
        self.deleted_edges.add(edge_idx)
        result += [edge_content] + self.traverse(nxt_idx, depth+1)

        return result


class AbstractASGOperator(ABC):
    """Operator for ASGs"""
    @abstractmethod
    def asg_to_pattern(self, asg: ASG):
        """Transforms the given ASG into a pattern (a string)"""

    @abstractmethod
    def pattern_to_asg(self, pattern: str):
        """Transforms the given pattern (a string) into an ASG"""
