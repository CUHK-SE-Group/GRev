import re
from mutator.mutator_helper import AbstractMutatorHelper


class RedisMutatorHelper(AbstractMutatorHelper):
    def parse_node_pattern(self, node_pattern: str, raw_node=False):
        node_pattern = node_pattern.strip()
        assert node_pattern.startswith("(")
        assert node_pattern.endswith(")")

        if raw_node:
            return node_pattern

        if node_pattern == "()":
            return None, set(), set()

        node_pattern = node_pattern.replace(' ', '')

        # Extract variable name, labels and properties
        match = re.match(r"\((.*?)(:(\w+(:\w+)*))?(\s*\{.*?\})?\)", node_pattern)
        var_name, labels, properties = match.group(1), match.group(2), match.group(5)

        # Process labels
        label_exprs = []
        if labels:
            label_exprs = labels[1:].split(":")  # remove the leading colon

        # Process properties
        prop_kv_exprs = []
        if properties:
            properties = properties.strip()[1:-1]  # remove leading/trailing spaces, braces
            for prop in properties.split(','):  # split on ','
                prop_kv_exprs.append(prop)

        return var_name, label_exprs, prop_kv_exprs

    def parse_path_pattern(self, path_pattern: str, raw_node=False):
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
                nodes.append(self.parse_node_pattern(node, raw_node))
            elif num_paren_balance == 1 and num_bracket_balance == 0 and \
                    char == '(' and (suffix.endswith("]-") or suffix.endswith("]->")):
                relationship = suffix.strip()
                suffix = char
                relationships.append(relationship)
            else:
                suffix += char

        assert len(nodes) == len(relationships) + 1
        return nodes, relationships

    def node_to_pattern(self, node):
        var, labels, properties = node
        assert (isinstance(var, str))
        assert (isinstance(labels, set))
        assert (isinstance(properties, set))

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
