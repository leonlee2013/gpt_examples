import gradio as gr
import whisper
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# starting_prompt = """You are an assistant.
# You can discuss with the user, or perform email tasks. Emails require subject, recipient, and body.
# You will receive either intructions starting with [Instruction] , or user input starting with [User]. Follow the instructions.
# """
#
# prompts = {'START': '[Instruction] Write WRITE_EMAIL if the user wants to write an email, "QUESTION" if the user has a precise question, "OTHER"  in any other case. Only write one word.',
#            'QUESTION': '[Instruction] If you can answer the question, write "ANSWER", if you need more information write MORE, if you cannot answer write "OTHER". Only write one word.',
#            'ANSWER': '[Instruction] Answer the user''s question',
#            'MORE': '[Instruction] Ask the user for more information as specified by previous intructions',
#            'OTHER': '[Instruction] Give a polite answer or greetings if the user is making polite conversation. Else, answer to the user that you cannot answer the question or do the action',
#            'WRITE_EMAIL': '[Instruction] If the subject or recipient or body is missing,  answer "MORE". Else if you have all the information answer "ACTION_WRITE_EMAIL | subject:subject, recipient:recipient, message:message". ',
#            'ACTION_WRITE_EMAIL': '[Instruction] The mail has been sent. Answer to the user to  tell the action is done'}
# actions = ['ACTION_WRITE_EMAIL']


starting_prompt = """你是一个助手。
你可以与用户讨论，或执行电子邮件任务。电子邮件要求需包括主题、收件人和正文。
你会收到以[Instruction]开始的指令，或以[User]开始的用户输入。请遵循指示。
"""
prompts = {
    'START': '[Instruction] 如果用户想写邮件，请回答"WRITE_EMAIL"；如果用户有明确的问题，请回答"QUESTION"；在其他情况下，请回答"OTHER"。请只写一个单词。',
    'QUESTION': '[Instruction] 如果你能回答问题，请写"ANSWER"；如果需要更多信息，请写"MORE"；如果不能回答，请写"OTHER"。只写一个单词。',
    'ANSWER': '[Instruction] 回答用户的问题。',
    'MORE': '[Instruction] 根据先前的指示询问用户更多信息。',
    'OTHER': '[Instruction] 如果用户进行礼貌性的谈话，请作出礼貌答复。否则，请告知用户无法回答问题或执行该动作。',
    'WRITE_EMAIL': '[Instruction] 如果主题、收件人或正文缺失，请回答 "MORE"。如果你有所有信息，请回答 "ACTION_WRITE_EMAIL | subject:主题, recipient:收件人, message:消息"。',
    'ACTION_WRITE_EMAIL': '[Instruction] 邮件已发送。告知用户该操作已完成。'
}
actions = ['ACTION_WRITE_EMAIL']


class Discussion:
    """
    A class representing a discussion with a voice assistant.

    Attributes:
        state (str): The current state of the discussion.
        messages_history (list): A list of dictionaries representing the history of messages in the discussion.
        client: An instance of the OpenAI client.
        stt_model: The speech-to-text model used for transcribing audio.

    Methods:
        generate_answer: Generates an answer based on the given messages.
        reset: Resets the discussion to the initial state.
        do_action: Performs the specified action.
        transcribe: Transcribes the given audio file.
        discuss_from_audio: Starts a discussion based on the transcribed audio file.
        discuss: Continues the discussion based on the given input.
    """

    def __init__(
            self, state='START',
            messages_history=None) -> None:
        self.previous_state = None
        if messages_history is None:
            messages_history = [{'role': 'user',
                                 'content': f'{starting_prompt}'}]
        self.state = state
        self.messages_history = messages_history
        self.client = OpenAI()
        self.stt_model = whisper.load_model("base")

    def generate_answer(self, messages):
        response = self.client.chat.completions.create(
            temperature=0,
            model="gpt-4-turbo",
            messages=messages)
        return (response.
                choices[0].message.content)

    def reset(self, start_state='START'):
        self.messages_history = [
            {'role': 'user', 'content': f'{starting_prompt}'}]
        self.state = start_state
        self.previous_state = None

    def reset_to_previous_state(self):
        self.state = self.previous_state
        self.previous_state = None

    def to_state(self, state):
        self.previous_state = self.state
        self.state = state

    def do_action(self, action):
        """
        Performs the specified action.

        Args:
            action (str): The action to perform.
        """
        print(f'DEBUG perform action={action}')
        pass

    def transcribe(self, file):
        transcription = self.stt_model.transcribe(file)
        return transcription['text']

    def discuss_from_audio(self, file):
        if file:
            # Transcribe the audio file and use the input to start the discussion
            return self.discuss(f'[User] {self.transcribe(file)}')
        # Empty output if there is no file
        return ''

    def discuss(self, input=None):
        if input is not None:
            print(f'DEBUG input={input}')
            self.messages_history.append({"role": "user", "content": input})

        # Generate a completion
        completion = self.generate_answer(
            self.messages_history +
            [{"role": "user", "content": prompts[self.state]}])
        print(f'DEBUG completion={completion} state={self.state}')
        # Is the completion an action ?
        if completion.split("|")[0].strip() in actions:
            action = completion.split("|")[0].strip()
            self.to_state(action)
            self.do_action(completion)
            print(f'DEBUG action={action} actions={actions} completion={completion}')
            # Continue discussion
            return self.discuss()
        # Is the completion a new state ?
        elif completion in prompts:
            self.to_state(completion)
            print(f'DEBUG completion={completion}')
            # Continue discussion
            return self.discuss()
        # Is the completion an output for the user ?
        else:
            self.messages_history.append(
                {"role": "assistant", "content": completion})
            if self.state != 'MORE':
                # Get back to start
                self.reset()
            else:
                # Get back to previous state
                self.reset_to_previous_state()
            return completion


if __name__ == '__main__':
    discussion = Discussion()
    #
    # gr.Interface(
    #     theme=gr.themes.Soft(),
    #     fn=discussion.discuss_from_audio,
    #     live=True,
    #     inputs=gr.Audio(sources="microphone", type="filepath"),
    #     outputs="text").launch()
    discussion.discuss('[User] 你好，我想写一封邮件给我的朋友。')
    discussion.discuss('[User] 主题是生日快乐。')
    discussion.discuss('[User] 收件人是张三。 祝你生日快乐, 一起顺利。就这么多了 邮箱是  zhang@123.com')
    discussion.discuss('[User] 没有了，非常感谢')
    print("history===>", discussion.messages_history)
    # discussion.discuss('[User] 请帮我完善邮件内容。')
    # discussion.discuss('[User] 张三，祝你生日快乐！祝你新的工作一切顺利！')




    # To use command line instead of Gradio, remove above code and use this instead:
    # while True:
    #     message = input('User: ')
    #     print(f'Assistant: {discussion.discuss(message)}')