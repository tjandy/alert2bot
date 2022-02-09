#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 2021/1/18

import requests
import json
import sys


def gettenant_access_token():
    tokenurl="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers={"Content-Type":"application/json"}
    data={
        "app_id":"cli_xxxxxx",
        "app_secret":"xxxxxx"

    }
    request=requests.post(url=tokenurl,headers=headers,json=data)
    tenant_access_token = json.loads(request.content)['tenant_access_token']
    return tenant_access_token


def getuserid(tenant_access_token, emails):
    userurl="https://open.feishu.cn/open-apis/user/v1/batch_get_id?emails={}".format(emails)
    headers={"Authorization":"Bearer %s"%tenant_access_token}
    request=requests.get(url=userurl,headers=headers)
    user_id = json.loads(request.content)
    user_id=json.loads(request.content)['data']['email_users'][emails][0]['user_id']
    # user_id = json.loads(request.content)['data']['mobile_users'][emails][0]['user_id']
    return user_id


def sendmes(user_id, chat_id, tenant_access_token, text):
    #向群里发送消息
    sendurl="https://open.feishu.cn/open-apis/message/v4/send/"
    headers={"Authorization":"Bearer %s"%tenant_access_token,"Content-Type":"application/json"}
    # data={"chat_id":chat_id,
    #     "msg_type":"text",
    #     "content":{
    #         "text":"%s<at user_id=\"%s\">test</at>"%(messages,user_id)
    #     }
    # }
    #给个人发送消息
    data={"user_id":user_id,
        "msg_type":"text",
        "content":{
            "text":"{}<at user_id=\"{}\">test</at>".format(text, user_id)
        }
    }
    request=requests.post(url=sendurl,headers=headers,json=data)
    print(request.content)


if __name__ == '__main__':
    tenant_access_token = gettenant_access_token()
    print(tenant_access_token)
    # user_id = getuserid(tenant_access_token, 'xxx@xxx.com')
    email_list = ['xxx@xxxxxx.com', 'xxxxxx@xxxxxx.com']
    user_ids = []
    for i in email_list:
        user_id = getuserid(tenant_access_token, i)
        user_ids.append(user_id)
    print(user_ids)
    text = sys.argv[1]
    # sendmes(user_id, '', tenant_access_token, text)
    for i in user_ids:
        sendmes(i, '', tenant_access_token,  text)

