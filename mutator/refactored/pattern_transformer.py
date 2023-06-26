import re
from mutator.refactored.schema import *


class PatternTransformer(AbstractASGOperator):
    """Given a node pattern,
    returns tuple (variable name, label expression, list of all the properties)"""
    @staticmethod
    def __parse_node_pattern(node_pattern: str):
        """
        :param node_pattern: the node pattern represented by a string
        :return: (variable name (a string), label expression (a string), property key-value expressions)
        """

        node_pattern = node_pattern.strip()
        assert node_pattern.startswith("(")
        assert node_pattern.endswith(")")

        # Regex patterns for a single node pattern (TODO)
        node_pattern_regex = re.compile(
            r'\((?P<var>[a-zA-Z_][a-zA-Z_0-9]*):?(?P<label_expr>[^{}]*){?(?P<properties>[^}]*)}?\)'
        )

        match = node_pattern_regex.match(node_pattern)
        if match:
            var = match.group('var')
            label_expr = match.group('label_expr').strip()
            properties = [prop.strip() for prop in match.group('properties').split(',') if prop.strip()]
            return (var, label_expr, properties)
        else:
            assert False

    @staticmethod
    def __parse_path_pattern(path_pattern: str):
        """
        :param path_pattern: the path pattern represented by a string
        :return: (list of nodes, list of relationships) in that order
        """

        path_pattern = path_pattern.strip()
        assert path_pattern.startswith("(")
        assert path_pattern.endswith(")")

        nodes = []
        relationships = []

        num_paren_balance = 0
        num_bracket_balance = 0
        suffix = ''

        for char in path_pattern:
            if char == '(':
                num_paren_balance += 1
            elif char == ')':
                num_paren_balance -= 1
            elif char == '[':
                num_bracket_balance += 1
            elif char == ']':
                num_bracket_balance -= 1

            if num_paren_balance == num_bracket_balance == 0 and char == ')':
                suffix += char
                node = suffix.strip()
                print(f'Node = {node}')
                suffix = ''
                nodes.append(PatternTransformer.__parse_node_pattern(node))
            elif num_paren_balance == 1 and num_bracket_balance == 0 and \
                char == '(' and (suffix.endswith("]-") or suffix.endswith("]->")):
                relationship = suffix.strip()
                print(f'Relationship = {relationship}')
                suffix = char
                relationships.append(relationship)
            else:
                suffix += char

        assert len(nodes) == len(relationships)+1
        return nodes, relationships

    @staticmethod
    def __parse_pattern(pattern: str):
        """
        :param pattern: the pattern represented by a string
        :return: (
            list of edges as (node, relationship, the other node),
            list of isolated nodes
        )
        """

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

                nodes, relationships = PatternTransformer.__parse_path_pattern(path_pattern)
                if len(nodes) > 1:
                    for i in range(len(nodes)-1):
                        edges.append((nodes[i], relationships[i], nodes[i+1]))
                elif len(nodes) == 1:
                    isolated_nodes.append(nodes[0])
                else:
                    assert False

        return edges, isolated_nodes

    def pattern_to_asg(self, pattern: str):
        """
        Transforms the given pattern to an ASG.
        Would not handle node patterns without variable names for now.
        :param pattern: the pattern represented by a string
        :return: the corresponding ASG (which is uniquely determined)
        """
        edges, isolated_nodes = self.__parse_pattern(pattern)

        asg = ASG()

        var2id = dict()
        num_vars = 0
        vars = []
        all_labels = []
        all_properties = []
        # Sort out all the variables
        def check_node(n):
            nonlocal num_vars
            nonlocal vars
            nonlocal all_labels
            nonlocal all_properties
            var, label, properties = n
            if var not in var2id.keys():
                idx = num_vars
                var2id[var] = num_vars
                num_vars += 1
                assert(len(var2id) == num_vars)
                vars.append(var)
                all_labels.append(set())
                all_properties.append(set())
            else:
                idx = var2id[var]

            all_labels[idx].add(label)
            for property in properties:
                all_properties[idx].add(property)

        for (st, rel, en) in edges:
            print(f'st = {st}')
            check_node(st)
            check_node(en)
        for n in isolated_nodes:
            check_node(n)

        print(f'Number of variables is {num_vars}')
        for idx in range(num_vars):
            print(f'var = {vars[idx]}, labels = {all_labels[idx]}, properties = {all_properties[idx]}')

        for idx in range(num_vars):
            asg.add_node(Node(idx, vars[idx], all_labels[idx], all_properties[idx]))

        for (st, rel, en) in edges:
            st_idx = var2id[st[0]]
            en_idx = var2id[en[0]]
            asg.add_edge(st_idx, en_idx, rel)

        return asg

    def asg_to_pattern(self, asg: ASG):
        return None

    def parse_node_pattern(self, node_pattern: str):
        return self.__parse_node_pattern(node_pattern)

    def parse_path_pattern(self, path_pattern: str):
        return self.__parse_path_pattern(path_pattern)
