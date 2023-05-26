import guidance
import re

from configs import config
from gdb_clients import Redis
from guidance.llms.transformers import Vicuna
from guidance.llms import OpenAI

# guidance.llm = Vicuna('/mnt/hardDisk1/fay/vicuna-7b-new/',endpoint="http://localhost:8000/v1")
# guidance.llm = OpenAI(model='LLaMa',endpoint="http://localhost:8000/v1")

def eliminate_useless_clauses(query):
    # we will use GPT-3 for most of the examples in this tutorial
    guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo", token="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")
    program = guidance('''
    {{#system~}}
    You are a helpful and terse assistant.
    {{~/system}}
    
    {{#user~}}
    This is a {{language}} language. 
    You need to simplify it by eliminating the useless brace, remove meaningless logic clauses.
    For example: '((x)>(y))' can be 'x>y'. '((((x)>(y)) AND ((z)>(x))) OR TRUE)' can be 'TRUE' 
    Do not answer the question yet.
    {{~/user}}
    {{#assistant~}}
    I understard your question.
    {{~/assistant}}
    {{#user~}}
    MATCH (n0)<-[r0 :T1]-(n1 :L3)<-[r1 :T5]-(n2 :L3), (n4 :L3)-[r3 :T1]->(n5), (n6 :L3)<-[r4 :T1]-(n7 :L0 :L4)<-[r5 :T1]-(n2 :L3) WHERE ((((((((((((r5.k40) AND (r4.k42)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r0.id) <> (r4.id))) AND ((r0.id) <> (r5.id))) AND ((r1.id) <> (r3.id))) AND ((r1.id) <> (r4.id))) AND ((r1.id) <> (r5.id))) AND ((r3.id) <> (r4.id))) AND ((r3.id) <> (r5.id))) AND ((r4.id) <> (r5.id))) MATCH (n8), (n11 :L3 :L4 :L2)-[r8 :T1]->(n5) WHERE ((r8.id) > -1) WITH (r8.k42) AS a0 ORDER BY a0 DESC WHERE ('Kf61I' > 'B') UNWIND [351095065, -998815964] AS a1 MATCH (n3)-[]->(n4)-[]->(n5) WHERE ('L' > 'D') OPTIONAL MATCH (n7 :L4)<-[]-(n2 :L3)-[]->(n1) WHERE ((n2.k21) < (n7.k26)) RETURN (n2.k23) AS a2, a1;
    {{~/user}}
    {{#assistant~}}
    MATCH (n0)<-[r0:T1]-(n1:L3)<-[r1:T5]-(n2:L3), (n4:L3)-[r3:T1]->(n5), (n6:L3)<-[r4:T1]-(n7:L0:L4)<-[r5:T1]-(n2:L3) WHERE (r5.k40 AND r4.k42 AND r0.id <> r1.id AND r0.id <> r3.id AND r0.id <> r4.id AND r0.id <> r5.id AND r1.id <> r3.id AND r1.id <> r4.id AND r1.id <> r5.id AND r3.id <> r4.id AND r3.id <> r5.id AND r4.id <> r5.id) MATCH (n8), (n11:L3:L4:L2)-[r8:T1]->(n5) WHERE r8.id > -1 WITH r8.k42 AS a0 ORDER BY a0 DESC WHERE 'Kf61I' > 'B' UNWIND [351095065, -998815964] AS a1 MATCH (n3)-->(n4)-->(n5) WHERE 'L' > 'D' OPTIONAL MATCH (n7:L4)<--(n2:L3)-->(n1) WHERE n2.k21 < n7.k26 RETURN n2.k23 AS a2, a1;
    {{~/assistant}}
    {{#user~}}
    {{query}}
    {{~/user}}
    {{#assistant~}}
    {{~gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}''')

    executed_program = program(language='cypher', query=query)
    print(executed_program['answer'])
    return executed_program['answer'].replace('\n', ' ')



def eliminate_useless_clauses2(query):
    from langchain.llms import OpenAI
    from langchain import PromptTemplate, LLMChain
    import os

    os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"

    llm = OpenAI(model="text-embedding-ada-002",temperature=0.1, openai_api_key='None', max_tokens=500) 
    
    h_template =  """
    This is a cypher language. 
    You need to simplify it by eliminating the **useless brace**, remove meaningless logic clauses.
    [[Example Question]]: [[MATCH (n0)<-[r0 :T1]-(n1 :L3)<-[r1 :T5]-(n2 :L3), (n4 :L3)-[r3 :T1]->(n5), (n6 :L3)<-[r4 :T1]-(n7 :L0 :L4)<-[r5 :T1]-(n2 :L3) WHERE ((((((((((((r5.k40) AND (r4.k42)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r0.id) <> (r4.id))) AND ((r0.id) <> (r5.id))) AND ((r1.id) <> (r3.id))) AND ((r1.id) <> (r4.id))) AND ((r1.id) <> (r5.id))) AND ((r3.id) <> (r4.id))) AND ((r3.id) <> (r5.id))) AND ((r4.id) <> (r5.id))) MATCH (n8), (n11 :L3 :L4 :L2)-[r8 :T1]->(n5) WHERE ((r8.id) > -1) WITH (r8.k42) AS a0 ORDER BY a0 DESC WHERE ('Kf61I' > 'B') UNWIND [351095065, -998815964] AS a1 MATCH (n3)-[]->(n4)-[]->(n5) WHERE ('L' > 'D') OPTIONAL MATCH (n7 :L4)<-[]-(n2 :L3)-[]->(n1) WHERE ((n2.k21) < (n7.k26)) RETURN (n2.k23) AS a2, a1;]]
    
    [[Example Answer]]: [[MATCH (n0)<-[r0:T1]-(n1:L3)<-[r1:T5]-(n2:L3), (n4:L3)-[r3:T1]->(n5), (n6:L3)<-[r4:T1]-(n7:L0:L4)<-[r5:T1]-(n2:L3) WHERE (r5.k40 AND r4.k42 AND r0.id <> r1.id AND r0.id <> r3.id AND r0.id <> r4.id AND r0.id <> r5.id AND r1.id <> r3.id AND r1.id <> r4.id AND r1.id <> r5.id AND r3.id <> r4.id AND r3.id <> r5.id AND r4.id <> r5.id) MATCH (n8), (n11:L3:L4:L2)-[r8:T1]->(n5) WHERE r8.id > -1 WITH r8.k42 AS a0 ORDER BY a0 DESC WHERE 'Kf61I' > 'B' UNWIND [351095065, -998815964] AS a1 MATCH (n3)-->(n4)-->(n5) WHERE 'L' > 'D' OPTIONAL MATCH (n7:L4)<--(n2:L3)-->(n1) WHERE n2.k21 < n7.k26 RETURN n2.k23 AS a2, a1;]]
    
    [[Real Question]]: [[{query}]]
    
    [[Real Answer]]: 
    """
    
    prompt = PromptTemplate(template=h_template, input_variables=["query"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    res = llm_chain.run(query)
    print(res)
    return ''









def eliminate_useless_clauses3(query):
    from langchain.llms import OpenAI
    from langchain import PromptTemplate, LLMChain

    llm = OpenAI(model="text-embedding-ada-002", openai_api_key='None', openai_api_base='http://localhost:8000/v1', max_tokens=500, temperature=0) 
    
    template =  """
    This is a {language} language. 
    You need to simplify it by eliminating the useless brace, remove meaningless logic clauses.
    For example: '((x)>(y))' can be 'x>y'. '((((x)>(y)) AND ((z)>(x))) OR TRUE)' can be 'TRUE' 
    You only output the simplified result like the example answer.
    [[Example Question]]: [[MATCH (n0)<-[r0 :T1]-(n1 :L3)<-[r1 :T5]-(n2 :L3), (n4 :L3)-[r3 :T1]->(n5), (n6 :L3)<-[r4 :T1]-(n7 :L0 :L4)<-[r5 :T1]-(n2 :L3) WHERE ((((((((((((r5.k40) AND (r4.k42)) AND ((r0.id) <> (r1.id))) AND ((r0.id) <> (r3.id))) AND ((r0.id) <> (r4.id))) AND ((r0.id) <> (r5.id))) AND ((r1.id) <> (r3.id))) AND ((r1.id) <> (r4.id))) AND ((r1.id) <> (r5.id))) AND ((r3.id) <> (r4.id))) AND ((r3.id) <> (r5.id))) AND ((r4.id) <> (r5.id))) MATCH (n8), (n11 :L3 :L4 :L2)-[r8 :T1]->(n5) WHERE ((r8.id) > -1) WITH (r8.k42) AS a0 ORDER BY a0 DESC WHERE ('Kf61I' > 'B') UNWIND [351095065, -998815964] AS a1 MATCH (n3)-[]->(n4)-[]->(n5) WHERE ('L' > 'D') OPTIONAL MATCH (n7 :L4)<-[]-(n2 :L3)-[]->(n1) WHERE ((n2.k21) < (n7.k26)) RETURN (n2.k23) AS a2, a1;]]
    [[Example Answer]]: [[MATCH (n0)<-[r0:T1]-(n1:L3)<-[r1:T5]-(n2:L3), (n4:L3)-[r3:T1]->(n5), (n6:L3)<-[r4:T1]-(n7:L0:L4)<-[r5:T1]-(n2:L3) WHERE (r5.k40 AND r4.k42 AND r0.id <> r1.id AND r0.id <> r3.id AND r0.id <> r4.id AND r0.id <> r5.id AND r1.id <> r3.id AND r1.id <> r4.id AND r1.id <> r5.id AND r3.id <> r4.id AND r3.id <> r5.id AND r4.id <> r5.id) MATCH (n8), (n11:L3:L4:L2)-[r8:T1]->(n5) WHERE r8.id > -1 WITH r8.k42 AS a0 ORDER BY a0 DESC WHERE 'Kf61I' > 'B' UNWIND [351095065, -998815964] AS a1 MATCH (n3)-->(n4)-->(n5) WHERE 'L' > 'D' OPTIONAL MATCH (n7:L4)<--(n2:L3)-->(n1) WHERE n2.k21 < n7.k26 RETURN n2.k23 AS a2, a1;]]
    [[Real Question]]: [[{query}]]
    please output [[Real Answer]], quoted with [[]]: 
    """
    
    prompt = PromptTemplate(template=template, input_variables=["language", "query"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    print(llm_chain.run(language='cypher',query=query))

    return ''
