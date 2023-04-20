from pattern_transformer import TransformASG2Pattern
from Pattern2ASG import TransformPattern2ASG


def TransformerPattern(pattern):
    G = TransformPattern2ASG(pattern)
    return TransformASG2Pattern(G)


if __name__ == "__main__":
    print(TransformerPattern(
        "(n0 :L3 :L6)<-[r0 :T0]-(n1)-[r1 :T3]->(n2 :L6 :L2 :L1), (n3 :L0)-[r2 :T0]->(n4 :L6)<-[r3 :T2]-(n5 :L1), (n3 :L0)<-[r4 :T0]-(n6 :L6 :L0)<-[r5 :T2]-(n7 :L4)"))
