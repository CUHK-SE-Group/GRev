import guidance

# we will use GPT-3 for most of the examples in this tutorial
guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo")


program = guidance('''This is a {{language}} language. 
                   You need to simplify it by eliminating the useless brace, remove unmeaningful clauses.
                   For example: '((x)>(y))' can be 'x>y'. '((((x)>(y)) AND ((z)>(x))) OR TRUE)' can be 'TRUE' 
                   Here you go:
                   {{query}}
                   {{~gen 'best' temperature=0.7 max_tokens=7}}
                   ''')

executed_program = program(language='cypher', query="MATCH (n0)<-[r0 :T1]-(n1 :L3)<-[r1 :T5]-(n2 :L3), (n4 :L3)-[r3 :T1]->(n5), (n6 :L3)<-[r4 :T1]-(n7 :L0 :L4)<-[r5 :T1]-(n2 :L3) WHERE ((((((((((((r5.k40) AND (r4.k42)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r0.id) <> (r4.id))) AND ((r0.id) <> (r5.id))) AND ((r1.id) <> (r3.id))) AND ((r1.id) <> (r4.id))) AND ((r1.id) <> (r5.id))) AND ((r3.id) <> (r4.id))) AND ((r3.id) <> (r5.id))) AND ((r4.id) <> (r5.id))) MATCH (n8), (n11 :L3 :L4 :L2)-[r8 :T1]->(n5) WHERE ((r8.id) > -1) WITH (r8.k42) AS a0 ORDER BY a0 DESC WHERE ('Kf61I' > 'B') UNWIND [351095065, -998815964] AS a1 MATCH (n3)-[]->(n4)-[]->(n5) WHERE ('L' > 'D') OPTIONAL MATCH (n7 :L4)<-[]-(n2 :L3)-[]->(n1) WHERE ((n2.k21) < (n7.k26)) RETURN (n2.k23) AS a2, a1;")

executed_program()