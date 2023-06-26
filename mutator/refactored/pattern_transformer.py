from mutator.refactored.schema import *


class PatternTransformer(AbstractASGOperator):
    def pattern_to_asg(self, pattern: str):
        """
        Transforms the given pattern to an ASG.
        Would not handle node patterns without variable names for now.
        :param pattern: the pattern represented by a string
        :return: the corresponding ASG (which is uniquely determined)
        """
        edges, isolated_nodes = parse_pattern(pattern)

        asg = ASG()

        var2id = dict()
        num_vars = 0
        all_vars = []
        all_labels = []
        all_properties = []

        # Sorts out all the variables
        def check_node(n):
            nonlocal num_vars
            nonlocal all_vars
            nonlocal all_labels
            nonlocal all_properties
            var, label, properties = n
            if var not in var2id.keys():
                idx = num_vars
                var2id[var] = num_vars
                num_vars += 1
                assert(len(var2id) == num_vars)
                all_vars.append(var)
                all_labels.append(set())
                all_properties.append(set())
            else:
                idx = var2id[var]

            all_labels[idx].add(label)
            for property in properties:
                all_properties[idx].add(property)

        for (st, rel, en) in edges:
            check_node(st)
            check_node(en)
        for n in isolated_nodes:
            check_node(n)

        for idx in range(num_vars):
            asg.add_node(Node(idx, all_vars[idx], all_labels[idx], all_properties[idx]))

        for (st, rel, en) in edges:
            st_idx = var2id[st[0]]
            en_idx = var2id[en[0]]
            asg.add_edge(st_idx, en_idx, rel)
            print(f'({st_idx}, {rel}, {en_idx})')

        return asg

    def asg_to_pattern(self, asg: ASG):
        """
        Transforms the given ASG into a pattern (in string).
        :param asg: the ASG given
        :return: a pattern in string (not deterministic due to the randomness of path elimination)
        """
        num_rounds = 0
        decomposition = []
        while True:
            if asg.is_empty():
                break
            start_idx = random.choice(asg.get_available_nodes())
            decomposition.append(asg.traverse(start_idx))

            # For test purpose
            assert num_rounds < 1000

        num_paths = len(decomposition)
        num_nodes = asg.get_num_nodes()
        locs = [[] for i in range(num_nodes)]
        for path_idx in range(num_paths):
            path = decomposition[path_idx]
            assert(len(path) % 2 == 1)
            for k in range(0, len(path), 2):
                assert(isinstance(path[k], int))
                node_idx = path[k]
                locs[node_idx].append((path_idx, k))
                # (Variable index, set of label expressions, set of property key-value expressions)
                path[k] = (asg.get_node_name(node_idx), set(), set())

        for node_idx in range(num_nodes):
            assert(len(locs[node_idx]) > 0)

            labels = asg.get_node_labels(node_idx)
            for label in labels:
                subset = get_nonempty_sample(locs[node_idx])
                for (path_idx, k) in subset:
                    decomposition[path_idx][k][1].add(label)

            properties = asg.get_node_properties(node_idx)
            for prop in properties:
                subset = get_nonempty_sample(locs[node_idx])
                for (path_idx, k) in subset:
                    decomposition[path_idx][k][2].add(prop)

    def parse_node_pattern(self, node_pattern: str):
        return parse_node_pattern(node_pattern)

    def parse_path_pattern(self, path_pattern: str):
        return parse_path_pattern(path_pattern)
