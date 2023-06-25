from mutator.refactored.pattern_transformer import *

def test_parse_node_pattern():
    pt = PatternTransformer()
    print(pt.parse_node_pattern("(n:(Person&Student) {name: 'Alice', age: 30})"))
    print(pt.parse_node_pattern("(n9:((L5)|L6|!!L5|!!(L1)) { p: 10, q: date('2023-02-10') })"))

def test_parse_path_pattern():
    pt = PatternTransformer()
    print(pt.parse_path_pattern("(n:Person)-[r:FRIEND]->(m:Person)<-[s:ENEMY]-(o:Person)"))
    print(pt.parse_path_pattern("(n9:(((L5)|L6|!!L5|!!(L1))) { p: 10, q: date('2023-02-10') })-[]-(n:HUMAN&DICK)"))
