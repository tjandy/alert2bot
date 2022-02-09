#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 12/11/20

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wind on 12/1/20


import requests
import logging
import falcon
import json

# 日志模块
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('connect.log', mode='w', encoding='UTF-8')
fileHandler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


# 处理从alertmanager接收过来的信息
def message_handler(message):
    # eval将结果转化成字典
    message = eval(message)
    return message


class Connect(object):
    def on_post(self, req, resp):
        messages = req.stream.read()
        logger.debug(messages)
        try:
            messages = str(bytes.decode(messages))
            logger.debug(messages)
            messages = message_handler(messages)
        except Exception as e:
            logger.debug(e)


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)


# 启动 nohup waitress-serve --port=23333 connect:app > alertmanager_wechatrobot.log &
# 需要安装waitress   pip install waitress