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


def create(tenant_access_token):
    url="https://www.feishu.cn/approval/openapi/v3/external/approval/create"
    headers={"Authorization":"Bearer %s"%tenant_access_token}
    data = {
    "approval_name": "@i18n@1",
    "approval_code": "XXXX-YYYY",
    "group_code": "XXXX-ZZZZ",
    "group_name": "@i8n@2",
    "external": {
        "create_link_pc": "http://",
        "create_link_mobile": "http://",
        "support_pc": True,
        "support_mobile": True,
        "support_batch_read": False
    },
    "viewers": [
        {
            "viewer_type": "TENANT"
        }
    ],
    "i18n_resources":[
     {
        "locale":"en-US",
        "is_default":True,
         "texts":{
            "@i18n@1":"people",
             "@i18n@2":"hr",
             "@i18n@3":"HR"
         }
      }
    ]
}

    request=requests.post(url=url,headers=headers,json=data)
    print(request)
    return request


if __name__ == '__main__':
    tenant_access_token = gettenant_access_token()
    create(tenant_access_token)

