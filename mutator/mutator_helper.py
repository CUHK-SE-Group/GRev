import random
from abc import ABC, abstractmethod


class AbstractMutatorHelper(ABC):
    @abstractmethod
    def parse_node_pattern(self, node_pattern: str, raw_node=False):
        pass

    @abstractmethod
    def parse_path_pattern(self, path_pattern: str, raw_node=False):
        pass

    @abstractmethod
    def node_to_pattern(self, node):
        pass

    def path_to_pattern(self, path, raw_node=False):
        """Given a path, returns its corresponding pattern"""
        result = ''
        if not raw_node:
            for k in range(len(path)):
                if k % 2 == 0:
                    # A node
                    result += self.node_to_pattern(path[k])
                else:
                    # A relationship
                    result += path[k]
        else:
            # Raw case
            for p in path:
                result += p
        return result

    def reverse_path(self, path_pattern: str):
        """Given a path pattern, returns the pattern written backward"""
        nodes, relationships = self.parse_path_pattern(path_pattern, True)
        assert len(nodes) > 0

        nodes.reverse()
        relationships.reverse()
        for k in range(len(relationships)):
            relationships[k] = self.flip_edge(relationships[k])

        path = []
        for k in range(len(relationships)):
            path.append(nodes[k])
            path.append(relationships[k])
        path.append(nodes[-1])
        return self.path_to_pattern(path, True)

    @staticmethod
    def flip_edge(edge: str):
        """Takes an edge as a string and flip its direction"""
        if edge.startswith("<"):
            return edge[1:] + ">"
        elif edge.endswith(">"):
            return "<" + edge[:-1]
        else:
            return edge

    @staticmethod
    def get_nonempty_sample(a):
        sz = len(a)
        assert sz > 0
        subset_sz = random.randint(1, sz)
        return random.sample(a, subset_sz)

    def parse_pattern(self, pattern: str, raw_node=False):
        pattern = pattern.strip()
        pattern += ','

        edges = []
        isolated_nodes = []

        num_paren_balance = 0
        num_bracket_balance = 0
        suffix = ''
        for char in pattern:
            suffix += char

            if char == '(':
                num_paren_balance += 1
            elif char == ')':
                num_paren_balance -= 1
            elif char == '[':
                num_bracket_balance += 1
            elif char == ']':
                num_bracket_balance -= 1

            if char == ',' and num_paren_balance == num_bracket_balance == 0:
                path_pattern = suffix.strip(',').strip()
                suffix = ''

                nodes, relationships = self.parse_path_pattern(path_pattern, raw_node)
                if len(nodes) > 1:
                    for i in range(len(nodes) - 1):
                        edges.append((nodes[i], relationships[i], nodes[i + 1]))
                elif len(nodes) == 1:
                    isolated_nodes.append(nodes[0])
                else:
                    assert False

        return edges, isolated_nodes
