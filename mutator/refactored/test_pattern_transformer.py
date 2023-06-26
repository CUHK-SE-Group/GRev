from mutator.refactored.pattern_transformer import *


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
