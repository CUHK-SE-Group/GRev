import re
import random


def flip_edge(edge: str):
    """Takes an edge as a string and flip its direction"""
    if edge.startswith("<"):
        return edge[1:] + ">"
    elif edge.endswith(">"):
        return "<" + edge[:-1]
    else:
        return edge
    

def parse_node_pattern(node_pattern: str):
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
        return var, label_expr, properties
    else:
        assert False


def parse_path_pattern(path_pattern: str):
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
            suffix = ''
            nodes.append(parse_node_pattern(node))
        elif num_paren_balance == 1 and num_bracket_balance == 0 and \
                char == '(' and (suffix.endswith("]-") or suffix.endswith("]->")):
            relationship = suffix.strip()
            suffix = char
            relationships.append(relationship)
        else:
            suffix += char

    assert len(nodes) == len(relationships)+1
    return nodes, relationships


def parse_pattern(pattern: str):
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

            nodes, relationships = parse_path_pattern(path_pattern)
            if len(nodes) > 1:
                for i in range(len(nodes) - 1):
                    edges.append((nodes[i], relationships[i], nodes[i + 1]))
            elif len(nodes) == 1:
                isolated_nodes.append(nodes[0])
            else:
                assert False

    return edges, isolated_nodes


def node_to_pattern(node):
    """
    (TODO)
    Given a node, returns its corresponding node pattern
    :param node: (variable name, set of label expressions, set
    of property key-value expressions).
    :return:
    """
    return None


def path_to_pattern(path):
    """
    Given a path, returns its corresponding pattern
    :param path: the alternating list of [node, relationship, node, ..., relationship, node],
    where nodes are of the form (variable name, set of label expressions, set of
    property key-value expressions).
    :return: the pattern string.
    """
    result = ''
    for k in range(path):
        if k % 2 == 0:
            # A node
            result += node_to_pattern(path[k])
        else:
            # A relationship
            result += path[k]
    return result


def reverse_path(path_pattern: str):
    """
    (NOT TESTED)
    Given a path pattern, returns the pattern written backward.
    :param path_pattern: the path pattern given
    :return: the pattern written backward
    """
    nodes, relationships = parse_path_pattern(path_pattern)
    nodes.reverse()
    relationships.reverse()
    if len(nodes) == 1:
        return nodes[0]
    elif len(nodes) > 1:
        result = ''
        for k in range(len(nodes)-1):
            result += nodes[k]
            result += flip_edge(relationships[k])
        result += nodes[-1]
        return result
    else:
        assert False


def get_nonempty_sample(a):
    sz = len(a)
    assert sz > 0
    subset_sz = random.randint(1, sz)
    return random.sample(a, subset_sz)
