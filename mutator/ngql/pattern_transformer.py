from mutator.ngql.schema import *


class PatternTransformer(AbstractASGOperator):
    def pattern_to_asg(self, pattern: str):
        """
        Transforms the given pattern to an ASG.
        Would not handle node patterns without variable names for now.
        :param pattern: the pattern represented by a string
        :return: the corresponding ASG (which is uniquely determined)
        """
        edges, isolated_nodes = NGQLMutatorHelper().parse_pattern(pattern)

        asg = ASG()

        var2id = dict()
        num_vars = 0
        all_vars = []
        all_properties = []

        # Sorts out all the variables
        def check_node(node):
            nonlocal num_vars
            nonlocal all_vars
            nonlocal all_properties
            var, properties = node
            if var not in var2id.keys():
                node_idx = num_vars
                var2id[var] = num_vars
                num_vars += 1
                assert(len(var2id) == num_vars)
                all_vars.append(var)
                all_properties.append(dict())
            else:
                node_idx = var2id[var]

            assert isinstance(properties, dict)

            for tag_name, tag_props in properties.items():
                assert isinstance(tag_props, set)
                if tag_name not in all_properties[node_idx]:
                    all_properties[node_idx][tag_name] = set()
                all_properties[node_idx][tag_name].update(tag_props)

        for (st, rel, en) in edges:
            check_node(st)
            check_node(en)
        for n in isolated_nodes:
            check_node(n)

        for idx in range(num_vars):
            asg.add_node(Node(idx, all_vars[idx], all_properties[idx]))

        for (st, rel, en) in edges:
            st_idx = var2id[st[0]]
            en_idx = var2id[en[0]]
            asg.add_edge(st_idx, en_idx, rel)

        return asg

    def asg_to_pattern(self, asg: ASG):
        """
        Transforms the given ASG into a pattern (in string).
        :param asg: the ASG given
        :return: a pattern in string (not deterministic due to the randomness of path elimination)
        """
        decomposition = []
        while True:
            if asg.is_empty():
                break
            start_idx = random.choice(asg.get_available_nodes())
            decomposition.append(asg.traverse(start_idx))

        num_paths = len(decomposition)
        num_nodes = asg.get_num_nodes()
        locations = [[] for _ in range(num_nodes)]
        for path_idx in range(num_paths):
            path = decomposition[path_idx]
            assert(len(path) % 2 == 1)
            for k in range(0, len(path), 2):
                assert(isinstance(path[k], int))
                node_idx = path[k]
                locations[node_idx].append([path_idx, k])
                # (variable index, dict of properties)
                path[k] = (asg.get_node_name(node_idx), dict())

        def update(properties, tag_name, prop=None):
            if tag_name not in properties:
                properties[tag_name] = set()
            if prop is not None:
                properties[tag_name].add(prop)

        for node_idx in range(num_nodes):
            assert(len(locations[node_idx]) > 0)

            properties = asg.get_node_properties(node_idx)
            for tag_name, tag_props in properties.items():
                for path_idx, k in NGQLMutatorHelper.get_nonempty_sample(locations[node_idx]):
                    update(decomposition[path_idx][k][1], tag_name)
                for prop in tag_props:
                    for path_idx, k in NGQLMutatorHelper.get_nonempty_sample(locations[node_idx]):
                        update(decomposition[path_idx][k][1], tag_name, prop)

        path_patterns = []
        for path in decomposition:
            path_patterns.append(NGQLMutatorHelper().path_to_pattern(path))
        assert len(path_patterns) > 0
        return ", ".join(path_patterns)
