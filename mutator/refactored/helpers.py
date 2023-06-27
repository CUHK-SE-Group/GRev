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
    :return: (variable name (a string), set of label expressions (a set of strings), set of property key-value expressions)
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
        labels = set(label.strip() for label in match.group('label_expr').strip().split(":") if label.strip())
        properties = set(prop.strip() for prop in match.group('properties').split(',') if prop.strip())
        return var, labels, properties
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
    Given a node, returns its corresponding node pattern
    :param node: (variable name, set of label expressions, set
    of property key-value expressions).
    :return:
    """
    var, labels, properties = node
    assert(isinstance(var, str))
    assert(isinstance(labels, set))
    assert(isinstance(properties, set))

    labels = list(labels)
    properties = list(properties)

    if len(labels) == 0 and len(properties) == 0:
        return "(" + var + ")"
    elif len(properties) == 0:
        return "(" + var + ":" + ":".join(labels) + ")"
    elif len(labels) == 0:
        return "(" + var + " " + "{" + ", ".join(properties) + "}" + ")"
    else:
        return "(" + var + ":" + ":".join(labels) + " " + "{" + ", ".join(properties) + "}" + ")"


def path_to_pattern(path):
    """
    Given a path, returns its corresponding pattern
    :param path: the alternating list of [node, relationship, node, ..., relationship, node],
    where nodes are of the form (variable name, set of label expressions, set of
    property key-value expressions).
    :return: the pattern string.
    """
    result = ''
    for k in range(len(path)):
        if k % 2 == 0:
            # A node
            result += node_to_pattern(path[k])
        else:
            # A relationship
            result += path[k]
    return result


def reverse_path(path_pattern: str):
    """
    Given a path pattern, returns the pattern written backward.
    :param path_pattern: the path pattern given
    :return: the pattern written backward
    """
    nodes, relationships = parse_path_pattern(path_pattern)
    assert len(nodes) > 0

    nodes.reverse()
    relationships.reverse()
    for k in range(len(relationships)):
        relationships[k] = flip_edge(relationships[k])

    path = []
    for k in range(len(relationships)):
        path.append(nodes[k])
        path.append(relationships[k])
    path.append(nodes[-1])
    return path_to_pattern(path)


def get_nonempty_sample(a):
    sz = len(a)
    assert sz > 0
    subset_sz = random.randint(1, sz)
    return random.sample(a, subset_sz)
