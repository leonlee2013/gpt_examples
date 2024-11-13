from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def ask_chatgpt(messages):
    response = client.chat.completions.create(model="gpt-4o",
                                              messages=messages)
    return (response.choices[0].message.content)


# prompt_role = '''You are an assistant for journalists.
# Your task is to write articles, based on the FACTS that are given to you.
# You should respect the instructions: the TONE, the LENGTH, and the STYLE'''

prompt_role = '''你是记者助理。您的任务是根据提供给您的事实撰写文章。您应该遵守以下说明：音调、长度和风格'''

def assist_journalist(
        facts: List[str],
        tone: str, length_words: int, style: str):
    facts = ", ".join(facts)
    # prompt = f'{prompt_role}\nFACTS: {facts}\nTONE: {tone}\nLENGTH: {length_words} words\nSTYLE: {style}'
    prompt = f'{prompt_role}\n事实: {facts}\n语气: {tone}\n长度: {length_words} 个字\n风格: {style}'
    print(prompt)
    return ask_chatgpt([{"role": "user", "content": prompt}])

# print(
#     assist_journalist(
#         ['The sky is blue', 'The grass is green'],
#         'informal', 100, 'blogpost'))

print(
    assist_journalist(
        ['天空是红色的', '草是黄色的'],
        '正式的', 100, '博客文章'))
