from mutator.refactored.pattern_transformer import *


def test_parse_node_pattern():
    pt = PatternTransformer()
    print(pt.parse_node_pattern("(n:(Person&Student) {name: 'Alice', age: 30})"))
    print(pt.parse_node_pattern("(n9:((L5)|L6|!!L5|!!(L1)) { p: 10, q: date('2023-02-10') })"))


def test_parse_path_pattern():
    pt = PatternTransformer()
    print(pt.parse_path_pattern("(n:Person)-[r:FRIEND]->(m:Person)<-[s:ENEMY]-(o:Person)"))
    print(pt.parse_path_pattern("(n9:(((L5)|L6|!!L5|!!(L1))) { p: 10, q: date('2023-02-10') })-[]-(bob:(L7&L5))"))


def test_transformer():
    pt = PatternTransformer()
    pt.pattern_to_asg("(n9:(((L5)|L6|!!L5|!!(L1))) { p: 10, q: date('2023-02-10') })-[]-(bob:(L7&L5))")

    with open('pattern_sample.in', 'r') as file:
        while True:
            pattern = file.readline()
            if pattern == '':
                break
            asg = pt.pattern_to_asg(pattern)
            pattern2 = pt.asg_to_pattern(asg)
            asg2 = pt.pattern_to_asg(pattern2)
            asg_c = asg.get_comparable()
            asg2_c = asg2.get_comparable()
            assert asg_c == asg2_c
            print(f'Pattern = {pattern}')
            print(f'Pattern2 = {pattern2}')
