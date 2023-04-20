import sys
from antlr4 import *
from CypherLexer import CypherLexer
from CypherParser import CypherParser
from CypherListener import CypherListener


class MyCypherListener(CypherListener):
    def enterOC_Match(self, ctx: CypherParser.OC_MatchContext):
        # 检查MATCH子句是否存在，存在则修改
        if ctx.MATCH():
            print(ctx)

    def exitOC_Match(self, ctx: CypherParser.OC_MatchContext):
        print(ctx)


def main(argv):
    input_stream = FileStream('test.stmt', encoding="utf-8")
    lexer = CypherLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = CypherParser(stream)
    tree = parser.oC_Cypher()  # 使用适当的入口规则

    # 创建一个新的MyCypherListener实例
    listener = MyCypherListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # 打印修改后的解析树
    print(tree.toStringTree(recog=parser))


if __name__ == '__main__':
    main(sys.argv)
