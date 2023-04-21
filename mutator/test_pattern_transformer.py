from mutator.pattern_transformer import *


def comparable_map(asg0):
    candidate0 = {}
    for i in asg0.Nodes:
        candidate0[i.content] = {}
        candidate0[i.content]["labels"] = i.labels
        candidate0[i.content]["name"] = i.name
        candidate0[i.content]["edges"] = {}
        for e in i.edges:
            del e['id']
            e['v'] = asg0.Nodes[e['v']].content
            candidate0[i.content]["edges"][e['content']] = e['content']
    return candidate0


def test_pattern2asg():
    with open('test_cases.ini', 'r') as file:
        line = file.readline()
        while line != '':
            p = PatternTransformer()
            pattern0 = line.replace('\n', '')
            asg0 = p.pattern2asg(pattern0)
            pattern1 = p.asg2pattern(asg0)
            asg1 = p.pattern2asg(pattern1)

            assert asg0.M == asg1.M
            assert asg0.N == asg1.N

            candidate0 = comparable_map(asg0)
            candidate1 = comparable_map(asg1)

            assert candidate0 == candidate1

            line = file.readline()


