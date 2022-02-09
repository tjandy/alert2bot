#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 12/1/20

from flask import Flask, request
import logging
import json
import requests

#python2 要加入如下
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


app = Flask(__name__)

# post请求格式json 例子：{"url":"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "message":"test"}
@app.route('/wechatbot', methods=["POST"])
def alertmanager():
    data = request.json
    url = data['url']
    message = data['message']
    try:
        logger.debug(message)
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        body = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        print(body)
        requests.post(url, json.dumps(body), headers=headers)
    except Exception as e:
        logger.debug(e)
    return 'send wechatbot'


@app.route('/feishubot', methods=["POST"])
def grafana():
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = request.get
    url = data['url']
    message = data['message']
    try:
        logger.debug(message)
        body1 = {
            "msg_type": "text",
            "content": {
                "text": message
            }
        }
        print(body1)
        requests.post(url, json.dumps(body1), headers=headers)
    except Exception as e:
        logger.debug(e)
    return 'send feishubot'


# @app.route('/mail', methods=["POST"])
# def grafana():
#     headers = {'Content-Type': 'application/json;charset=utf-8'}
#     data = request.json
#     url = data['url']
#     message = data['message']
#     try:
#         logger.debug(message)
#         body1 = {
#             "msg_type": "text",
#             "content": {
#                 "text": message
#             }
#         }
#         print(body1)
#         requests.post(url, json.dumps(body1), headers=headers)
#     except Exception as e:
#         logger.debug(e)
#     return 'send mail'


# 日志模块
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('message2all.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)




if __name__ == '__main__':
    app.run(debug=True)

# nohup gunicorn -b 0.0.0.0:23333 message2all:app > gunicorn.log 2>&1 &
# nohup gunicorn -w 2 -b 0.0.0.0:23333 message2all:app > gunicorn.log 2>&1 &
