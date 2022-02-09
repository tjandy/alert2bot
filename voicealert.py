#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/8
import sys

from aliyunsdkcore.client import AcsClient
from aliyunsdkdyvmsapi.request.v20170525.SingleCallByTtsRequest import SingleCallByTtsRequest
from aliyunsdkdyvmsapi.request.v20170525.SingleCallByVoiceRequest import SingleCallByVoiceRequest


# request1 = SingleCallByVoiceRequest()
# request1.set_accept_format('json')
# request1.set_CalledShowNumber("18850505050")
# request1.set_CalledNumber("15750505050")
# request1.set_VoiceCode("e271f3f2-e155-4366-a9f4-0fe55765b3ec.wav")
# response1 = client.do_action_with_exception(request1)
# print('发起语音文件通知返回')
# print(response1)
def send_voice(callednumber, message):
    client = AcsClient('xxxxxx', 'xxxxxxxxx')
    request2 = SingleCallByTtsRequest()
    request2.set_accept_format('json')
    request2.set_CalledShowNumber('')
    request2.set_CalledNumber(callednumber)
    request2.set_TtsCode("TTS_209162455")
    # request2.set_TtsParam("{\"name\":\"测试\",\"time\":\"2019年\"}")
    params = str({"content": message})
    request2.set_TtsParam(params)
    response2 = client.do_action_with_exception(request2)
    message = request2
    print('文本转语音类型返回')
    print(response2, type(request2))

if __name__ == '__main__':
    message = sys.argv[1]
    callednumbers = ['xxxxxx', 'xxxxxx']
    for i in callednumbers:
        send_voice(i, message)


