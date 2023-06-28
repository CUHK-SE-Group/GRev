from mutator.ngql.pattern_transformer import *


def test_transformer():
    pt = PatternTransformer()

    with open('pattern_sample.in', 'r') as file:
        while True:
            pattern = file.readline()
            if pattern == '':
                break
            print(f'Tested pattern = {pattern}')
            asg = pt.pattern_to_asg(pattern)
            pattern2 = pt.asg_to_pattern(asg)
            print(f'Transformed pattern = {pattern}')
            asg2 = pt.pattern_to_asg(pattern2)
            assert asg.get_comparable() == asg2.get_comparable()


# def test_path_reverser():
#     pt = PatternTransformer()
#
#     with open('path_pattern_sample.in', 'r') as file:
#         while True:
#             pattern = file.readline()
#             if pattern == '':
#                 break
#             rpattern = reverse_path(pattern)
#             asg = pt.pattern_to_asg(pattern)
#             rasg = pt.pattern_to_asg(rpattern)
#             assert asg.get_comparable() == rasg.get_comparable()
