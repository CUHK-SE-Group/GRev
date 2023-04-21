with open('database0-0.log', 'r') as f:
    content = f.read()

# 找到CREATE和MATCH语句的分界点
create_end_index = content.index('CREATE')
match_start_index = content.index('MATCH')

# 分离CREATE和MATCH语句
create_statements = content[create_end_index:match_start_index].strip().split(';')
match_statements = content[match_start_index:].strip().split(';')

# 输出结果
print('CREATE statements:')
print(''.join(create_statements))
print('MATCH statements:')
print(''.join(match_statements))
