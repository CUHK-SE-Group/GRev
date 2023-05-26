import re

def simplify_logic_expression(expression):
    # 匹配重复的括号并消除
    pattern = r'\(([^()]+)\)'
    while re.search(pattern, expression):
        expression = re.sub(pattern, r'\1', expression)

    return expression

# 示例表达式
expression = "((((((((((((r5.k40) AND (r4.k42)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r0.id) <> (r4.id))) AND ((r0.id) <> (r5.id))) AND ((r1.id) <> (r3.id))) AND ((r1.id) <> (r4.id))) AND ((r1.id) <> (r5.id))) AND ((r3.id) <> (r4.id))) AND ((r3.id) <> (r5.id))) AND ((r4.id) <> (r5.id)))"

# 调用函数简化表达式
simplified_expression = simplify_logic_expression(expression)

print("简化后的表达式：", simplified_expression)
