from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from openai import OpenAI

client = OpenAI()


def chat_completion(content, model="gpt-4", temperature=0, response_format=None):
    ret = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=temperature,
        response_format=response_format
    )
    return ret.choices[0].message.content


# template = """Question: {question}
# Let's think step by step.
# Answer: """
# prompt = PromptTemplate(template=template, input_variables=["question"])
template = """问题: {question}
 让我们一步一步来思考。
答案: """
prompt = PromptTemplate(template=template, input_variables=["question"])

llm = ChatOpenAI(model_name="gpt-4o")

# llm = ChatOpenAI(model_name="gpt-4")
llm_chain = LLMChain(prompt=prompt, llm=llm)

# question = """ What is the population of the capital of the country where the
# Olympic Games were held in 2016? """
question = """2016年举行奥运会的国家的首都人口是多少？"""
ret = llm_chain.invoke(question, verbose=True)
# print(llm_chain)
print('============>>>final ret:', ret)
# 答案: """
# ret2 = chat_completion(q, model="gpt-4o")
# print(q)
# print(ret2)
