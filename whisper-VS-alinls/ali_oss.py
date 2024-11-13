# -*- coding: utf-8 -*-

import os
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
# 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
# 填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# endpoint = "https://oss-cn-hangzhou.aliyuncs.com"
endpoint = os.getenv('ALIYUN_OSS_END_POINT')
bucketName = os.getenv('ALIYUN_OSS_BUCKET')
# 填写Endpoint对应的Region信息，例如cn-hangzhou。注意，v4签名下，必须填写该参数
# region = "cn-hangzhou"
region="cn-shanghai"

# yourBucketName填写存储空间名称。
bucket = oss2.Bucket(auth, endpoint, bucketName, region=region)

# 上传文件到OSS。
# yourObjectName由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
# yourLocalFile由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
bucket.put_object_from_file('d/asr/story.txt', '/Users/liyong/github/gpt_examples/Chap3_04_VoiceAssistant/story.txt')