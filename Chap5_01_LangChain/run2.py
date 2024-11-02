from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import load_tools, create_react_agent, AgentExecutor
from openai import OpenAI

client = OpenAI()


def chat_completion(content, model="gpt-3.5-turbo", temperature=0, response_format=None):
    ret = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=temperature,
        response_format=response_format
    )
    return ret.choices[0].message.content


question = """2016年举行奥运会的国家的首都人口的平方根是多少？"""
ret = chat_completion(question)
print("------------------>>>", ret)


llm = ChatOpenAI(model_name="gpt-3.5-turbo")
tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=hub.pull("hwchase17/react"),
)
# question = """What is the square root of the population of the capital of the
#  country where the Olympic Games were held in 2016 ?"""
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
ret2 = agent_executor.invoke({"input": question})
print('final ret2:', ret2)
