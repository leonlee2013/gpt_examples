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
    ret = client.fine_tuning.jobs.list()
    print(ret)
    return ret


# 取消微调作业
def cancel_fine_tune(fine_tune_id):
    # ret = client.fine_tuning.jobs.retrieve(fine_tune_id)
    ret = client.fine_tuning.jobs.cancel(fine_tune_id)
    print(ret)
    return ret


# //模型微调
def fine_tune(training_file, model="gpt-4o-mini-2024-07-18", suffix="direct_marketing"):
    ret = client.fine_tuning.jobs.create(training_file=training_file, model=model, suffix=suffix)
    print(ret)
    return ret


# client.fine_tuning.jobs.create(
#     training_file="file-abc123",
#     model="gpt-4o-mini-2024-07-18"
# )

# print(aa)
# aa = client.files.create(file=open("./out_openai_completion_prepared.jsonl", "rb"), purpose='fine-tune')
# ft_file = upload_file("./out_openai_completion2_prepared.jsonl")
# fine_tune(training_file=ft_file.id)
# fine_tune('file-UW2xCj4KLU7mAt7n6hBhVOoi')

# ftjob-7icIfkfrlnEnMdEOlfTwneJg
# delete_file('file-A8T0ibgdf39NTQTMrXIugKfH')
# list_files()
# ftjob-pUGpGUKJD7lZjCaQNnfSDS7i
print('=====================================')
list_fine_tunes()
print('=====================================')
# cancel_fine_tune('ftjob-APTJn2zxwMIklFe1BM1y4eJT')
