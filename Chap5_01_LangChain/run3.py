from time import sleep

from dotenv import load_dotenv

load_dotenv()
from langchain.chains import ConversationChain
from langchain_openai import OpenAI

chatbot_llm = OpenAI(model_name='gpt-3.5-turbo-instruct')
chatbot = ConversationChain(llm=chatbot_llm, verbose=True)
chatbot.predict(input='你好')
chatbot.predict(input='我可以问你一个问题吗？你是人工智能吗？')
chatbot.predict(input='你好')
print(chatbot)
