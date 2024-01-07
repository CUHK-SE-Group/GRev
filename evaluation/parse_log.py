def get_num(line: str, var: str):
    N = len(line)
    loc = line.find(var)
    if loc != -1:
        while not line[loc].isdigit():
            loc += 1
        cur = line[loc]
        loc += 1
        while loc < N and line[loc].isdigit():
            cur += line[loc]
            loc += 1
        return int(cur)
    else:
        return 0

if __name__ == '__main__':
    num_logic, num_performance = 0, 0
    with open('./eval1_final.log') as f:
        for line in f:
            cur_num_logic, cur_num_performance = get_num(line=line, var='#logic'), get_num(line=line, var='#performance')
            if cur_num_logic > 0 or cur_num_performance > 0:
                print((cur_num_logic, cur_num_performance))
                num_logic += cur_num_logic
                num_performance += cur_num_performance
    print((num_logic, num_performance))