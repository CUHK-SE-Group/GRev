import re
from mutator.mutator_helper import AbstractMutatorHelper


class RefactoredMutatorHelper(AbstractMutatorHelper):
    @staticmethod
    def parse_label_expressions(label_exprs: str):
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

    def parse_node_pattern(self, node_pattern: str, raw_node=False):
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
                labels = set(RefactoredMutatorHelper.parse_label_expressions(label_exprs))

            properties = set()
            if match.group('properties'):
                properties = set(prop.strip() for prop in match.group('properties').split(',') if prop.strip())

            if no_var_name:
                assert var == "z"
                var = None

            return var, labels, properties
        else:
            assert False

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
            return "(" + var + ":" + "&".join(labels) + ")"
        elif len(labels) == 0:
            return "(" + var + " " + "{" + ", ".join(properties) + "}" + ")"
        else:
            return "(" + var + ":" + "&".join(labels) + " " + "{" + ", ".join(properties) + "}" + ")"
