
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
client = OpenAI()

# Read the transcript from the file
with open("files/transcript.txt", "r") as f:
    transcript = f.read()

# Call the openai ChatCompletion endpoint, with the ChatGPT model
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user",
               # "content": f"Summarize the following video transcript.: \n{transcript}"}])
               "content": f"总结以下视频文字: \n{transcript}"}])


print(response.choices[0].message.content)
