from openai import OpenAI

client = OpenAI()


def generate_response(facts, user_question):
    prompt = '根据事实，回答问题。' + f'问题: {user_question}. 事实: {facts}'
    print(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ])
    # extract the response
    return response.choices[0].message.content


class ResponseService:
    def __init__(self):
        pass

        # messages=[
        #     {"role": "user", "content": 'Based on the FACTS, give an answer to the QUESTION.'+
        #                                 f'QUESTION: {user_question}. FACTS: {facts}'}
        # ])

