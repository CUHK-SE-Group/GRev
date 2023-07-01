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


def parse_single_tag(props: str):
    """(tag name, set of properties)"""
    props = props.strip()
    if props.endswith("}"):
        tokens = props.split("{")
        assert len(tokens) == 2
        name = tokens[0].strip()
        props_part = tokens[1].strip("}").split(",")
        return name, set([p.strip() for p in props_part])
    else:
        return props, set()


def parse_props(props: str):
    num_curly_balance = 0
    locs = []
    for i in range(len(props)):
        char = props[i]
        if char == '{':
            num_curly_balance += 1
        elif char == '}':
            num_curly_balance -= 1

        if char == ':' and num_curly_balance == 0:
            locs.append(i)

    result = dict()
    def update(stuff):
        name, prop_set = stuff
        assert not name.startswith(":")
        assert not name.endswith(":")
        nonlocal result
        result[name] = prop_set

    if len(locs) == 0:
        update(parse_single_tag(props))
    else:
        update(parse_single_tag(props[:locs[0]]))
        for j in range(len(locs)-1):
            x, y = locs[j], locs[j+1]
            update(parse_single_tag(props[x+1:y]))
        update(parse_single_tag(props[locs[-1]+1:]))

    return result


def parse_node_pattern(node_pattern: str, raw_node=False):
    """
    :param node_pattern: the node pattern represented by a string
    :return: (variable name (a string), dict of properties)
    """

    node_pattern = node_pattern.strip()
    assert node_pattern.startswith("(")
    assert node_pattern.endswith(")")

    if raw_node:
        return node_pattern

    node_pattern = node_pattern.strip("(").strip(")")
    assert node_pattern != ''

    first = node_pattern.find(":")
    if first == -1:
        var = node_pattern.strip()
        return var, dict()

    var = node_pattern[:first]

    tag_part = node_pattern[first+1:]

    return var, parse_props(tag_part)



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
    :param node: (variable name, dict of properties)
    :return:
    """
    var, properties = node
    assert(isinstance(var, str))
    assert(isinstance(properties, dict))

    if len(properties) == 0:
        return "(" + var + ")"

    result = "(" + var
    for tag_name, tag_props in properties.items():
        result += ":" + tag_name
        if len(tag_props) > 0:
            result += "{" + ", ".join(list(tag_props)) + "}"
    result += ")"
    return result

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
