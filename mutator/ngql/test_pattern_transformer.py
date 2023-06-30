from mutator.ngql.pattern_transformer import *


def test_simple():
    pt = PatternTransformer()
    with open('pattern_sample.in', 'r') as f:
        while True:
            pattern = f.readline()
            if pattern == '':
                break
            print(parse_pattern(pattern))
            asg = pt.pattern_to_asg(pattern)
            pattern2 = pt.asg_to_pattern(asg)
            asg2 = pt.pattern_to_asg(pattern2)
            print(f'pattern = {pattern}')
            print(f'pattern2 = {pattern2}')
            assert asg.get_comparable() == asg2.get_comparable()
