import random
import re
from mutator.refactored.schema import *

class PatternTransformer(AbstractASGOperator):
    """Given a node pattern,
    returns tuple (variable name, label expression, list of all the properties)"""
    def __parse_node_pattern(self, node_pattern: str):
        assert str != ''

        # Regex patterns for a single node pattern (TODO)
        node_pattern_regex = re.compile(
            r'\((?P<var>[a-zA-Z_][a-zA-Z_0-9]*):?(?P<label_expr>[^{}]*){?(?P<properties>[^}]*)}?\)'
        )

        match = node_pattern_regex.match(node_pattern)
        if match:
            var = match.group('var')
            label_expr = match.group('label_expr').strip()
            properties = [prop.strip() for prop in match.group('properties').split(',') if prop.strip()]
            return {
                'var': var,
                'label_expr': label_expr,
                'properties': properties
            }
        else:
            raise ValueError(f"Invalid node pattern: {node_pattern}")

    """Given a path pattern,
        returns the list of tuples (node, relationship, the other node)"""
    def __parse_path_pattern(self, path_pattern: str):
        assert path_pattern != ''

        nodes = []
        relationships = []

        num_paren_balance = 0
        num_bracket_balance = 0
        suffix = ''
        for char in path_pattern:
            suffix += char

            if char == '(':
                num_paren_balance += 1
            elif char == ')':
                num_paren_balance -= 1
            elif char == '[':
                num_bracket_balance += 1
            elif char == ']':
                num_bracket_balance -= 1

            if suffix.endswith(")") and num_paren_balance == 0 and num_bracket_balance == 0:
                nodes.append(suffix)
                suffix = ''
            elif (suffix.endswith("]-") or suffix.endswith("]->")) and num_bracket_balance == 0:
                relationships.append(suffix)
                suffix = ''

        assert len(nodes) == len(relationships)+1

        return nodes, relationships

    def pattern_to_asg(self, pattern: str):
        return None

    def asg_to_pattern(self, asg: ASG):
        return None

    def parse_node_pattern(self, node_pattern: str):
        return self.__parse_node_pattern(node_pattern)

    def parse_path_pattern(self, path_pattern: str):
        return self.__parse_path_pattern(path_pattern)