from openai import OpenAI

client = OpenAI()


def get_intent(user_question: str):
    # call the openai ChatCompletion endpoint
    prompt = f'从以下问题中提取关键字: {user_question}' + '不要回答任何其他内容，只回答关键字。'
    print(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "user", "content": prompt}
                                              ])

    # extract the response
    return response.choices[0].message.content


class IntentService:
    def __init__(self):
        pass

        # messages=[
        #       {"role": "user", "content": f'Extract the keywords from the following question: {user_question}'+
        #         'Do not answer anything else, only the keywords.'}
        #    ])

