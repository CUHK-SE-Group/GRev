import guidance
import re

from configs import config
from gdb_clients import Redis


def eliminate_useless_clauses(query):
    # we will use GPT-3 for most of the examples in this tutorial
    guidance.llm = guidance.llms.transformers.Vicuna("your_path/vicuna_13B", device_map="auto")
    # guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo", token="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")
    program = guidance('''
    {{#system~}}
    You are a helpful and terse assistant.
    {{~/system}}
    
    {{#user~}}
    This is a {{language}} language. 
    You need to simplify it by eliminating the useless brace, remove meaningless logic clauses.
    For example: '((x)>(y))' can be 'x>y'. '((((x)>(y)) AND ((z)>(x))) OR TRUE)' can be 'TRUE' 
    Here you go:
    {{query}}
    {{~/user}}
    
    {{#assistant~}}
    {{~gen 'answer' temperature=0 max_tokens=500}}
    {{~/assistant}}''')

    executed_program = program(language='cypher', query=query)
    return executed_program['answer'].replace('\n', ' ')






