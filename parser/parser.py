import json
import sys
from antlr4 import *
from CypherLexer import CypherLexer
from CypherParser import CypherParser
from CypherParser import ParseTreeVisitor


class ParseTreeVisitor1(ParseTreeVisitor):
    def __init__(self):
        self.errors = []

    def visit(self, tree):
        return tree.accept(self)

    def visitChildren(self, node):
        self.errors.append([])
        result = self.defaultResult()
        for i in range(node.getChildCount()):
            child = node.getChild(i)
            childResult = child.accept(self)
            print(childResult)

            result = self.aggregateResult(result, child, childResult)
        errors = self.errors.pop()
        return {
            'result': result,
            'errors': errors,
        }

    def visitTerminal(self, node):
        return {
            'parent': node.parentCtx.__class__.__name__.split('.')[-1][3:-7],
            'text': node.getText(),
            'sourceInterval': node.getSourceInterval(),
        }

    def visitErrorNode(self, node):
        self.errors[-1].append(self.visitTerminal(node))
        return self.defaultResult()

    def defaultResult(self):
        return []

    def aggregateResult(self, aggregate, child, nextResult):
        aggregate.append({
            'node': self.visitTerminal(child),
            'children': nextResult,
        })
        return aggregate


def parse(query_string):
    input_stream = InputStream(query_string)
    lexer = CypherLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.oC_Cypher()
    visitor = ParseTreeVisitor1()
    result = visitor.visit(tree)
    return result


if __name__ == '__main__':
    # tree = parse('MATCH (n0 :L1 :L5)<-[r0 :T3]-(n1 :L3)-[r1 :T3]->(n2 :L1), (n2 :L5)<-[r2 :T4]-(n1) WHERE (((((r0.id) > -1) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r2.id))) AND ((r1.id) <> (r2.id))) UNWIND [(n1.k24)] AS a0 OPTIONAL MATCH (n2 :L1)<-[]-(n1 :L3) RETURN a0')
    tree = parse('MATCH (n) RETURN Count(n);')
    print(tree)
