from openai import OpenAI
import json

client = OpenAI()


def chat_completion(content, model="gpt-4", temperature=0, response_format=None):
    ret = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        temperature=temperature,
        response_format=response_format
    )
    return ret.choices[0].message.content


def the_reviewer(prompt_initialization, current_prompt):
    prompt_reviewer = prompt_initialization + "\n\n"
    # prompt_reviewer += f"This is my prompt: {current_prompt}\n\n"
    # prompt_reviewer += """Task: Provide a detailed, rigorous critique of my prompt. To do this, first start by giving
    # my prompt a score from 0 to 5 (0 for poor, 5 for very optimal), and then write a short paragraph detailing
    # improvements that would make my prompt a perfect prompt with a score of 5."""
    prompt_reviewer += f"这是我的提示: {current_prompt}\n\n"
    prompt_reviewer += """任务： 对我的提示进行详细、严谨的评论。为此，请先给我的提示 
    从 0 到 5 分给我的提示打分（0 分代表差，5 分代表非常好），然后写一小段话，详细说明如何改进我的提示，使其成为 5 分的完美提示。
    改进措施，使我的提示语成为 5 分的完美提示语。"""
    reviews = chat_completion(prompt_reviewer)
    return reviews


def the_questioner(prompt_initialization, current_prompt, reviews, questions_answers):
    prompt_questioner = prompt_initialization + "\n\n"
    # prompt_questioner += f"This is my prompt: {current_prompt}\n\n"
    # prompt_questioner += f"A critical review of my prompt:{reviews}\n\n"
    # prompt_questioner += """Task: Compile a list of maximum 4 sort questions whose answers are indispensable for
    # improving my prompt (also give examples of answers in baskets.). Output format: In JSON format. The output must
    # be accepted by json.loads. The json format should be like: {'Questions': ['Question 1','Question 2','Question 3',
    # 'Question 4']}"""
    prompt_questioner += f"这是我的提示: {current_prompt}\n\n"
    prompt_questioner += f"这是对我当前提示的关键评审：{reviews}\n\n"
    prompt_questioner += """任务：编制最多4个排序问题的列表，这些问题的答案对于改善我的提示至关重要（并且提供每个问题的示例答案）。
    输出格式：JSON格式。输出格式应可被json.loads接受。JSON
    格式应为：{'Questions': ['问题1','问题2','问题3','问题4']}"""

    questions_json = chat_completion(prompt_questioner, model="gpt-4-1106-preview",
                                     response_format={"type": "json_object"})

    try:
        questions = json.loads(questions_json).get('Questions', [])
    except json.JSONDecodeError:
        print("Failed to decode questions from the model's response.")
        questions = []

    for i, question in enumerate(questions, start=1):
        answer = input(f"Question {i}: {question} ")
        questions_answers = questions_answers + f"Question: {question}\nAnswer:{answer}\n\n"

    return questions_answers


def the_prompt_maker(prompt_initialization, current_prompt, reviews, questions_answers):
    maker_prompt = prompt_initialization + "\n\n"
    # maker_prompt += f"This is my current prompt: {current_prompt}\n\n"
    # maker_prompt += f"This is critical review of my current prompt:{reviews}\n\n"
    # maker_prompt += f"Some questions and answers for improving my current prompt:{questions_answers}\n\n"
    # maker_prompt += """Task: With all of this information, use all of your prompt engineering expertise to rewrite my
    # current prompt in the best possible way to create a perfect prompt for GPT with a score of 5. All the information
    # contained in the questions and answers must be included in the new prompt. Start the prompt by assigning one or
    # many roles to GPT, defining the context, and the task. Output: It's very important that you only return the new
    # prompt for GPT that you've created, and nothing else."""
    maker_prompt += f"这是我当前的提示： {current_prompt}\n\n"
    maker_prompt += f"这是对我当前提示的关键评审：{reviews}\n\n"
    maker_prompt += f"一些用于改善我当前提示的问题和答案：{questions_answers}\n\n"
    maker_prompt += """任务：利用所有这些信息，运用你所有的提示工程专业知识，以最佳方式重写我当前的提示，创建一个得分为5的完美提示。
    新提示中必须包含问题和答案中的所有信息。首先为GPT分配一个或多个角色，定义上下文和任务。
    输出：非常重要的是，你只需返回你创建的新提示，不要其他任何内容。"""

    new_prompt = chat_completion(maker_prompt)
    return new_prompt


def prompter(initial_prompt, max_nb_iter=3):
    print(f"Your initial prompt: {initial_prompt}")

    # prompt_initialization = """You are an expert in prompt engineering and large language models. A good prompt
    # should assign one or many roles to GPT, define a clear context and task, and clarify expected output. You know
    # and use many prompt techniques such as: Few-Shot Learning, Prompt Chaining, Shadow Prompting, ... I want you to
    # be my personal prompt creator expert. Your name is now 'Prompter' and that is how I will address you from now
    # on. Prompter and GPT are separate and distinct entities. You, Prompter, are responsible for creating good
    # prompts for GPT."""

    prompt_initialization = """你是提示工程和大型语言模型的专家。
一个好的提示应该为GPT分配一个或多个角色，定义清晰的上下文和任务，并明确期望的输出。
你知道并使用许多提示技术，如：少量示例学习（Few-Shot Learning）、提示链（Prompt Chaining）、影子提示（Shadow Prompting）等。
我希望你成为我的个人提示创建专家。 你的名字现在是“Prompter”，我将从现在起这样称呼你。
Prompter和GPT是两个独立的实体。 你，Prompter，负责为GPT创建好的提示。"""

    current_prompt = initial_prompt
    questions_answers = ""
    for i in range(max_nb_iter):

        print(f"Loop {i + 1}")
        reviews = the_reviewer(prompt_initialization, current_prompt)
        print("reviews-------------------------------------------------")
        print(f"reviews: {reviews}")
        print("reviews-------------------------------------------------")
        questions_answers = the_questioner(prompt_initialization, current_prompt, reviews, questions_answers)
        print("questions_answers-------------------------------------------------")
        print(f"questions_answers: {questions_answers}")
        print("questions_answers-------------------------------------------------")
        current_prompt = the_prompt_maker(prompt_initialization, current_prompt, reviews, questions_answers)
        print(f"\nNew current prompt: {current_prompt}\n\n")
        keep = input(f"Do you want to keep this prompt (y/n)? ")
        if keep == 'y':
            break

    return current_prompt


# "Give me a suggestion for the main course for today's lunch."
prompt = prompter("请给我一个关于今天午餐主菜的建议。", max_nb_iter=3)
res = chat_completion(prompt)
print(res)
