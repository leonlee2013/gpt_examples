import gradio as gr
import whisper
import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
import json
import time
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import librosa
import soundfile as sf
from datetime import datetime

auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
endpoint = os.getenv('ALIYUN_OSS_END_POINT')
bucketName = os.getenv('ALIYUN_OSS_BUCKET')
region = "cn-shanghai"
bucket = oss2.Bucket(auth, endpoint, bucketName, region=region)
# bucket.put_object_from_file('d/asr/story.txt', '/Users/liyong/github/gpt_examples/Chap3_04_VoiceAssistant/story.txt')

# stt_model = whisper.load_model("base")
stt_model = whisper.load_model("large-v3")


def ali_asr_transcribe(fileLink):
    print("fileLink:", fileLink)
    accessKeyId = os.getenv('ALIYUN_AK_ID')
    accessKeySecret = os.getenv('ALIYUN_AK_SECRET')
    appKey = os.getenv('NLS_APP_KEY')
    # 地域ID，固定值。
    REGION_ID = "cn-shanghai"
    PRODUCT = "nls-filetrans"
    DOMAIN = "filetrans.cn-shanghai.aliyuncs.com"
    API_VERSION = "2018-08-17"
    POST_REQUEST_ACTION = "SubmitTask"
    GET_REQUEST_ACTION = "GetTaskResult"
    # 请求参数
    KEY_APP_KEY = "appkey"
    KEY_FILE_LINK = "file_link"
    KEY_VERSION = "version"
    KEY_ENABLE_WORDS = "enable_words"
    # 是否开启智能分轨
    KEY_AUTO_SPLIT = "auto_split"
    # 响应参数
    KEY_TASK = "Task"
    KEY_TASK_ID = "TaskId"
    KEY_STATUS_TEXT = "StatusText"
    KEY_RESULT = "Result"
    # 状态值
    STATUS_SUCCESS = "SUCCESS"
    STATUS_RUNNING = "RUNNING"
    STATUS_QUEUEING = "QUEUEING"
    # 创建AcsClient实例
    client = AcsClient(accessKeyId, accessKeySecret, REGION_ID)
    # 提交录音文件识别请求
    postRequest = CommonRequest()
    postRequest.set_domain(DOMAIN)
    postRequest.set_version(API_VERSION)
    postRequest.set_product(PRODUCT)
    postRequest.set_action_name(POST_REQUEST_ACTION)
    postRequest.set_method('POST')
    task = {KEY_APP_KEY: appKey, KEY_FILE_LINK: fileLink, KEY_VERSION: "4.0", KEY_ENABLE_WORDS: False}
    task = json.dumps(task)
    print(task)
    postRequest.add_body_params(KEY_TASK, task)
    taskId = ""
    try:
        postResponse = client.do_action_with_exception(postRequest)
        postResponse = json.loads(postResponse)
        print(postResponse)
        statusText = postResponse[KEY_STATUS_TEXT]
        if statusText == STATUS_SUCCESS:
            print("录音文件识别请求成功响应！")
            taskId = postResponse[KEY_TASK_ID]
        else:
            print("录音文件识别请求失败！")
            return
    except ServerException as e:
        print(e)
    except ClientException as e:
        print(e)
    # 创建CommonRequest，设置任务ID。
    getRequest = CommonRequest()
    getRequest.set_domain(DOMAIN)
    getRequest.set_version(API_VERSION)
    getRequest.set_product(PRODUCT)
    getRequest.set_action_name(GET_REQUEST_ACTION)
    getRequest.set_method('GET')
    getRequest.add_query_param(KEY_TASK_ID, taskId)
    # statusText = ""
    while True:
        try:
            getResponse = client.do_action_with_exception(getRequest)
            getResponse = json.loads(getResponse)
            print(getResponse)
            statusText = getResponse[KEY_STATUS_TEXT]
            if statusText == STATUS_RUNNING or statusText == STATUS_QUEUEING:
                # 继续轮询
                time.sleep(1)
            else:
                # 退出轮询
                break
        except ServerException as e:
            print(e)
        except ClientException as e:
            print(e)
    if statusText == STATUS_SUCCESS:
        print(getResponse)
        # 提取并合并所有的文本
        # text = getResponse.get("Result", {}).get("Sentences", [{}])[0].get("Text", "No Text Found")
        combined_text = ' '.join(sentence['Text'] for sentence in getResponse['Result']['Sentences'])
        print("aliyunnls==========>", combined_text)
        return combined_text
    else:
        print("录音文件识别失败============>>>>>", statusText)
        return "录音文件识别失败！"


def ali_nls_transcribe(file):
    dir_path, file_name = os.path.split(file)
    new_file_name = f"d/asr/{file_name}"
    bucket.put_object_from_file(new_file_name, file)
    url = "http://lilith-imv2-cn.oss-cn-shanghai.aliyuncs.com"
    return ali_asr_transcribe(f"{url}/{new_file_name}")


def whisper_transcribe(file):
    transcription = stt_model.transcribe(file)
    print(transcription)
    print("whisper==========>:", transcription['text'])
    return transcription['text']


def resample(audio_file):
    # 加载音频文件，sr=None 保证读取原始采样率
    audio, sr = librosa.load(audio_file, sr=None)

    # 目标采样率
    target_sr = 16000

    # 获取当前日期，格式为 YYYY-MM-DD
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 提取文件名和扩展名
    base_name = audio_file.rsplit('.', 1)[0]  # 去掉文件扩展名
    extension = audio_file.rsplit('.', 1)[1]  # 获取文件扩展名

    # 构造新的文件名，加入日期
    output_file = f"{base_name}_{date_str}.{extension}"

    # 如果当前采样率不是目标采样率，则进行转换
    if sr != target_sr:
        print(f"Audio converted from {sr} to {target_sr}.")
        # 将采样率转换为目标采样率
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr

        # 将转换后的音频保存为新的文件
        sf.write(output_file, audio, sr)
        print(f"Resampled audio saved to {output_file}.")
    else:
        print("No resampling needed, sample rate is already 16000.")
    return output_file

def discuss_from_audio(file):
    if file:
        out_file = resample(file)
        print(f'DEBUG out_file={out_file}')
        whisper_text = whisper_transcribe(out_file)
        ali_nls_text = ali_nls_transcribe(out_file)
        return f'[whisper :] {whisper_text}\n[aliyunnls:] {ali_nls_text}'
    # Empty output if there is no file
    return ''


if __name__ == '__main__':
    gr.Interface(
        theme=gr.themes.Soft(),
        fn=discuss_from_audio,
        live=True,
        inputs=gr.Audio(sources="microphone", type="filepath"),
        outputs="text"        # 可自定义端口号
    # ).launch(server_name="0.0.0.0", server_port=7860)
    ).launch()
