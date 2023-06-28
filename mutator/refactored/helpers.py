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
    
    
def parse_label_expressions(label_exprs: str):
    """Parses label expressions; expressions are separated
    by '&''s."""

    label_exprs = label_exprs.strip()
    assert label_exprs.startswith("(")
    assert label_exprs.endswith(")")

    num_paren_balance = 0
    suffix = ''
    result = []
    for char in label_exprs:
        suffix += char
        if char == '(':
            num_paren_balance += 1
        elif char == ')':
            num_paren_balance -= 1

        if num_paren_balance == 0:
            if char == ')':
                expr = suffix.strip()
                assert expr.startswith("(")
                assert expr.endswith(")")
                result.append(expr)
            suffix = ''
    return result


def parse_node_pattern(node_pattern: str, raw_node=False):
    """
    :param node_pattern: the node pattern represented by a string
    :return: (variable name (a string), set of label expressions (a set of strings),
    set of property key-value expressions)
    """

    node_pattern = node_pattern.strip()
    assert node_pattern.startswith("(")
    assert node_pattern.endswith(")")

    if raw_node:
        return node_pattern

    if node_pattern == "()":
        return None, set(), set()

    # Forgive me
    no_var_name = False
    if node_pattern.startswith("(:"):
        no_var_name = True
        node_pattern = node_pattern[:1] + "z" + node_pattern[1:]

    # Regex patterns for a single node pattern
    node_pattern_regex = re.compile(
        r'\((?P<var>[a-zA-Z_][a-zA-Z_0-9]*)(?:\s*\:\s*(?P<label_exprs>\([^{}]*\)(\s*&\s*\([^{}]*\))*))?\s*{?(?P<properties>[^}]*)}?\)'
    )

    match = node_pattern_regex.match(node_pattern)
    if match:
        var = match.group('var')

        labels = set()
        if match.group('label_exprs'):
            label_exprs = match.group('label_exprs')
            labels = set(parse_label_expressions(label_exprs))

        properties = set()
        if match.group('properties'):
            properties = set(prop.strip() for prop in match.group('properties').split(',') if prop.strip())

        if no_var_name:
            assert var == "z"
            var = None

        return var, labels, properties
    else:
        assert False


def parse_path_pattern(path_pattern: str, raw_node=False):
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
            nodes.append(parse_node_pattern(node, raw_node))
        elif num_paren_balance == 1 and num_bracket_balance == 0 and \
                char == '(' and (suffix.endswith("]-") or suffix.endswith("]->")):
            relationship = suffix.strip()
            suffix = char
            relationships.append(relationship)
        else:
            suffix += char

    assert len(nodes) == len(relationships)+1
    return nodes, relationships


def parse_pattern(pattern: str, raw_node=False):
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

            nodes, relationships = parse_path_pattern(path_pattern, raw_node)
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
        return "(" + var + ":" + "&".join(labels) + ")"
    elif len(labels) == 0:
        return "(" + var + " " + "{" + ", ".join(properties) + "}" + ")"
    else:
        return "(" + var + ":" + "&".join(labels) + " " + "{" + ", ".join(properties) + "}" + ")"


def path_to_pattern(path, raw_node=False):
    """
    Given a path, returns its corresponding pattern
    :param path: the alternating list of [node, relationship, node, ..., relationship, node],
    where nodes are of the form (variable name, set of label expressions, set of
    property key-value expressions).
    :return: the pattern string.
    """
    result = ''
    if not raw_node:
        for k in range(len(path)):
            if k % 2 == 0:
                # A node
                result += node_to_pattern(path[k])
            else:
                # A relationship
                result += path[k]
    else:
        # Raw case
        for p in path:
            result += p
    return result


def reverse_path(path_pattern: str):
    """
    Given a path pattern, returns the pattern written backward.
    :param path_pattern: the path pattern given
    :return: the pattern written backward
    """
    nodes, relationships = parse_path_pattern(path_pattern, True)
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
    return path_to_pattern(path, True)


def get_nonempty_sample(a):
    sz = len(a)
    assert sz > 0
    subset_sz = random.randint(1, sz)
    return random.sample(a, subset_sz)
