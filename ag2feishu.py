#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 12/1/20
import ast

import requests
import logging
import falcon
import json
#python2 要加入如下
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# 飞书机器人链接
feishu_boot_url = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"

# 日志模块
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('ag2feishu.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

# 时间转换 最新版本输出过来的是utc时间，之前有的老版本输出过来的是+8的时间，后缀会有+8：00
# 新 开始时间: 2020-12-30T03:35:07.319648556Z 结束时间: 0001-01-01T00:00:00Z
# 老 开始时间: 2020-12-01T06:13:37.319648556+08:00 结束时间: 0001-01-01T00:00:00Z
# 适配三者 如果是老版本的有加8到时候+8改成+0就行了 可以按照自己需要调整时间
def utc_s(utc):
    origin_date_str = utc.strip().split('+')[0].split('.')[0].replace('Z', '').split('T')
    date = origin_date_str[0]
    time = origin_date_str[1].split(':')
    hour = int(time[0]) + 8
    if hour > 24:
        hour = hour - 24
    min, sec = time[1], time[2]
    return '{} {}:{}:{}'.format(date, hour, min, sec)


# 处理从alertmanager接收过来的信息
def message_handler(message):
    # ast.literal_eval() str--> dict
    message = ast.literal_eval(message)
    alerts = message["alerts"]
    alert_message = []
    # 需要注意多实例的情况
    # 新 {"receiver":"default_alert","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"InstanceDown","instance":"192.16.77.98:50000","job":"node_ops","severity":"warning","type":"instance"},"annotations":{"description":"192.16.77.98:50000 of job node_ops has been down for more than 3 minutes.","summary":"Instance 192.16.77.98:50000 down"},"startsAt":"2020-12-30T03:34:07.319648556Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://ali-prometheus:9090/graph?g0.expr=up+%3D%3D+0\u0026g0.tab=1","fingerprint":"f4eecae10e3e0bb3"},{"status":"firing","labels":{"alertname":"InstanceDown","instance":"192.16.77.99:50000","job":"node_ops","severity":"warning","type":"instance"},"annotations":{"description":"192.16.77.99:50000 of job node_ops has been down for more than 3 minutes.","summary":"Instance 192.16.77.99:50000 down"},"startsAt":"2020-12-30T03:35:07.319648556Z","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://ali-prometheus:9090/graph?g0.expr=up+%3D%3D+0\u0026g0.tab=1","fingerprint":"22a95b0dcdd9fb5e"}],"groupLabels":{"alertname":"InstanceDown"},"commonLabels":{"alertname":"InstanceDown","job":"node_ops","severity":"warning","type":"instance"},"commonAnnotations":{},"externalURL":"http://ali-prometheus:9093","version":"4","groupKey":"{}/{}:{alertname=\"InstanceDown\"}","truncatedAlerts":0}
    # 旧 {"receiver":"default_alert","status":"firing","alerts":[{"status":"firing","labels":{"alertname":"InstanceDown","instance":"192.168.155.92:50000","job":"node_iproxy","severity":"warning","type":"instance"},"annotations":{"description":"192.168.155.92:50000 of job node_iproxy has been down for more than 3 minutes.","summary":"Instance 192.168.155.92:50000 down"},"startsAt":"2020-12-01T06:13:37.319648556+08:00","endsAt":"0001-01-01T00:00:00Z","generatorURL":"http://ops15588:9090/graph?g0.expr=up+%3D%3D+0\u0026g0.tab=1","fingerprint":"94bfa30ddc7ac25d"}],"groupLabels":{"type":"instance"},"commonLabels":{"alertname":"InstanceDown","instance":"192.168.155.92:50000","job":"node_iproxy","severity":"warning","type":"instance"},"commonAnnotations":{"description":"192.168.155.92:50000 of job node_iproxy has been down for more than 3 minutes.","summary":"Instance 192.168.155.92:50000 down"},"externalURL":"http://ops15588:9093","version":"4","groupKey":"{}/{}:{type=\"instance\"}"}
    for i in range(len(alerts)):
        alert = alerts[i]
        alert = ast.literal_eval(str(alert))
        status = alert["status"]
        labels = alert["labels"]
        annotations = alert["annotations"]
        startsAt = utc_s(alert["startsAt"])
        endsAt = utc_s(alert["endsAt"])
        alertname = ast.literal_eval(str(labels))["alertname"]
        instance = ast.literal_eval(str(labels))["instance"]
        severity = ast.literal_eval(str(labels))["severity"]
        description = ast.literal_eval(str(annotations))["description"]
        message = "------------------------------" + '\n' \
                  + "           alertmanager"  + '\n' \
                  + "------------------------------" + '\n' \
                  + "状态: " + status + '\n' \
                  + "报警名称: " + alertname + '\n' \
                  + "报警实例: " + instance + '\n'  \
                  + "报警等级: " + severity + '\n' \
                  + "报警描述: " + description + '\n' \
                  + "开始时间: " + startsAt + '\n' \
                  + "结束时间: " + endsAt + '\n' \
                  + "------------------------------"
        alert_message.append(message)
    return alert_message
# ------------------------------
#            alertmanager告警
# ------------------------------
# 状态: firing
# 告警名字: InstanceDown
# 告警实例: 192.168.155.92:50000
# 告警等级: firing
# 告警描述: 192.168.155.92:50000 of job node_iproxy has been down for more than 3 minutes.
# 开始时间: 2020-12-01T06:13:37.319648556+08:00
# 结束时间: 0001-01-01T00:00:00Z
# ------------------------------

# 发送到飞书的函数
def sendfeishu(botmessage):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    logger.debug(botmessage)
    body = {
        "msg_type": "text",
        "content": {
            "text": botmessage
        }
    }
    requests.post(feishu_boot_url, json.dumps(body), headers=headers)

# alertmanager post请求处理函数
class feishubot(object):
    def on_post(self, req, resp):
        messages = req.stream.read()
        logger.debug(messages)
        try:
            messages = str(bytes.decode(messages))
            logger.debug(messages)
            messages = message_handler(messages)
            for i in range(len(messages)):
                sendfeishu(str(messages[i]))
        except Exception as e:
            logger.debug(e)


app = falcon.API()
feishubot = feishubot()
app.add_route('/feishubot', feishubot)

# pip install requests falcon waitress
# 启动 nohup waitress-serve --port=23333 ag2feishu:app > alertmanager_wechatrobot.log &
# 需要安装waitress   pip install waitress
