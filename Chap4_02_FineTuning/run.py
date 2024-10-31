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


# ret = chat_completion("请给我一个关于今天午餐主菜的建议。")
# print(ret)

# **上传文件：**
def upload_file(file_path, purpose='fine-tune'):
    ret = client.files.create(file=open(file_path, "rb"), purpose=purpose)
    print(ret)
    return ret


# **删除文件**
def delete_file(file_id):
    ret = client.files.delete(file_id)
    print(ret)
    return ret


# 列出所有的文件
def list_files():
    ret = client.files.list()
    print(ret)
    return ret


# 列出微调作业
def list_fine_tunes():
    ret = client.fine_tuning.list()
    print(ret)
    return ret


# 取消微调作业
def cancel_fine_tune(fine_tune_id):
    ret = client.fine_tuning.cancel(fine_tune_id)
    print(ret)
    return ret


# upload_file("./out_openai_completion_prepared.jsonl")
# print(aa)
# aa = client.files.create(file=open("./out_openai_completion_prepared.jsonl", "rb"), purpose='fine-tune')
# delete_file('file-pOkiBRHbWx108BJ7cyLP5cJV')
list_files()
list_fine_tunes()
