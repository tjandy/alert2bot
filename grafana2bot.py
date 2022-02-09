#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 12/1/20

from flask import Flask, request
import logging
import json
import requests

#python2 要加入如下  原因python3 区分了 unicode str 和 byte arrary，并且默认编码不再是 ascii Python的str默认是ascii编码，和unicode编码冲突
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


app = Flask(__name__)

@app.route('/grafana', methods=["POST"])
def alertmanager():
    grafana_message = request.get_data()
    print(grafana_message)
    logger.debug(grafana_message)
    try:
        logger.debug(grafana_message)
        botmessage = message_handler(grafana_message)
        send_wechat(botmessage)
    except Exception as e:
        logger.debug(e)
    return 'OK'
# 微信机器人链接
wechat_boot_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxx"

# 日志模块
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('grafana2wechatbot.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# 处理从grafana接收过来的信息
# {
#     "dashboardId":1,
#     "evalMatches":[
#         {
#             "value":100,
#             "metric":"High value",
#             "tags":null
#         },
#         {
#             "value":200,
#             "metric":"Higher Value",
#             "tags":null
#         }
#     ],
#     "message":"Someone is testing the alert notification within grafana.",
#     "orgId":0,
#     "panelId":1,
#     "ruleId":0,
#     "ruleName":"Test notification",
#     "ruleUrl":"http://localhost:3000/",
#     "state":"alerting",
#     "tags":{
#
#     },
#     "title":"[Alerting] Test notification"
# }

def message_handler(grafana_message):
    messages = json.loads(grafana_message)
    title = messages['title']
    state = messages['state']
    ruleName = messages['ruleName']
    ruleUrl = messages['ruleUrl']
    message = messages['message']
    botmessage = "------------------------------" + '\n' \
              + "           grafana"  + '\n' \
              + "------------------------------" + '\n' \
              + "title: " + title + '\n' \
              + "state: " + state + '\n' \
              + "ruleName: " + ruleName + '\n'  \
              + "ruleUrl: " + ruleUrl + '\n' \
              + "message: " + message + '\n' \
              + "------------------------------"
    return botmessage

# 发送到微信里的函数
def send_wechat(botmessage):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    logger.debug(botmessage)
    body = {
        "msgtype": "text",
        "text": {
            "content": botmessage
        }
    }
    print(str(body))
    requests.post(wechat_boot_url, json.dumps(body), headers=headers)



if __name__ == '__main__':
    app.run(debug=True)


# nohup gunicorn -w 2 -b 0.0.0.0:23333 alertmanager2bot:app > gunicorn.log 2>&1 &