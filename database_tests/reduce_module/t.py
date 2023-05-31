from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import openai

embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
# wget https://raw.githubusercontent.com/hwchase17/langchain/master/docs/modules/state_of_the_union.txt
loader = TextLoader('state_of_the_union.txt')
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])

llm = OpenAI(model="vicuna-7b-v1.1") # select your faux openai model name
# llm = OpenAI(model="gpt-3.5-turbo")

questions = [
             "who is the speaker",
             "What did the president say about Ketanji Brown Jackson",
             "What are the threats to America",
             "Who are mentioned in the speech",
             "Who is the vice president",
             "How many projects were announced",
            ]

for query in questions:
    print("Query: ", query)
    print("Ans: ",index.query(query,llm=llm))