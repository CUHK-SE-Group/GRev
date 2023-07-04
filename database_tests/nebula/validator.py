from gdb_clients import *
from database_tests.nebula.TestNebula import compare
import time

log_file = "./query_producer/nebula/1688376693.9743934.log"

with open(log_file, 'r') as f:
    create_statements = f.read()
    f.close()
create_statements = create_statements.split("\n")

client = Nebula("validate", True)

pre_idx = 0
for i, v in enumerate(create_statements):
    if v == 'SLEEP':
        client.batch_run(create_statements[pre_idx:i])
        pre_idx = i+1
        time.sleep(7)
    else:
        continue

res1 = client.run("MATCH (n1:L1:L5)-[r1]-(n2), (n3:L3:L0)-[:T3]->(n4:L2) RETURN *")

res2 = client.run("MATCH (n4:L2)<-[:T3]-(n3:L3:L0), (n1:L1:L5)-[r1]-(n2) RETURN *")


eq = compare(res1[0], res2[0])
print(eq)