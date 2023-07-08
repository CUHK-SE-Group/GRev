from mutator.mutator_helper import AbstractMutatorHelper


class NGQLMutatorHelper(AbstractMutatorHelper):
    @staticmethod
    def parse_single_tag(props: str):
        props = props.strip()
        if props.endswith("}"):
            tokens = props.split("{")
            assert len(tokens) == 2
            name = tokens[0].strip()
            props_part = tokens[1].strip("}").split(",")
            return name, set([p.strip() for p in props_part])
        else:
            return props, set()

    @staticmethod
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
            update(NGQLMutatorHelper.parse_single_tag(props))
        else:
            update(NGQLMutatorHelper.parse_single_tag(props[:locs[0]]))
            for j in range(len(locs) - 1):
                x, y = locs[j], locs[j + 1]
                update(NGQLMutatorHelper.parse_single_tag(props[x + 1:y]))
            update(NGQLMutatorHelper.parse_single_tag(props[locs[-1] + 1:]))

        return result

    def parse_node_pattern(self, node_pattern: str, raw_node=False):
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
        tag_part = node_pattern[first + 1:]
        return var, NGQLMutatorHelper.parse_props(tag_part)

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
        var, properties = node
        assert (isinstance(var, str))
        assert (isinstance(properties, dict))

        if len(properties) == 0:
            return "(" + var + ")"

        result = "(" + var
        for tag_name, tag_props in properties.items():
            result += ":" + tag_name
            if len(tag_props) > 0:
                result += "{" + ", ".join(list(tag_props)) + "}"
        result += ")"
        return result
