#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import time
import base64

import qqbot
from qqbot.core.util.yaml_util import YamlUtil

from command_register import command

config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yml"))
ROOT = "{}:{}".format(config["host"], config["port"])
CHAT_URL = ROOT + "/chat"
OP_URL = ROOT + "/operate"
T_TOKEN = qqbot.Token(config["bot"]["appid"], config["bot"]["token"])

async def _send_message(content: str, event: str, message: qqbot.Message):
    """
    机器人发送消息
    """
    msg_api = qqbot.AsyncMessageAPI(T_TOKEN, False)
    dms_api = qqbot.AsyncDmsAPI(T_TOKEN, False)

    send = qqbot.MessageSendRequest(content, message.id)
    if event == "DIRECT_MESSAGE_CREATE":
        await dms_api.post_direct_message(message.guild_id, send)
    else:
        await msg_api.post_message(message.channel_id, send)

async def _chat(content, event, message):
    param = {
        "validate": config["validate"],
        "type": "text",
        "query": content,
        "uuid": str(int(time.time())),
    }
    r = requests.post(CHAT_URL, data=param)
    r.encoding = "utf-8"
    try:
        resp = r.json()["resp"]
        await _send_message("wukong: %s" % (resp), event, message)
    except Exception as e:
        qqbot.logger.error(e) 


def get_menu():
    return """功能菜单：
/打开勿扰模式
    打开勿扰模式
/关闭勿扰模式
    关闭勿扰模式
/播放音乐
    播放本地音乐
/结束音乐
    结束播放本地音乐
/下一首歌
    切到下一首歌
/上一首歌
    切到上一首歌
/拍照
    拍张照片
/清空缓存
    清除运行时产生的所有临时数据
/echo 内容
    远程给家里发语音消息
    示例：/echo 你是最棒的
"""

@command("/菜单")
async def ask_menu(param: str, event: str, message: qqbot.Message):
    ret = get_menu()
    await _send_message(ret, event, message)
    return True

@command("/我的id")
async def my_id(param: str, event: str, message: qqbot.Message):
    await _send_message('你的频道用户id为：%s' % message.author.id, event, message)
    return True

@command("/播放音乐")
async def play_music(param: str, event: str, message: qqbot.Message):
    await _chat('播放本地音乐', event, message)
    return True

@command("/打开勿扰模式")
async def switch_on_do_not_bother(param: str, event: str, message: qqbot.Message):
    param = {
        "validate": config["validate"],
        "type": "1"
    }
    r = requests.post(OP_URL, data=param)
    r.encoding = "utf-8"
    try:
        resp = r.json()["message"]
        await _send_message("wukong: %s" % (resp), event, message)
    except Exception as e:
        qqbot.logger.error(e) 
    return True

@command("/关闭勿扰模式")
async def switch_off_do_not_bother(param: str, event: str, message: qqbot.Message):
    param = {
        "validate": config["validate"],
        "type": "2"
    }
    r = requests.post(OP_URL, data=param)
    r.encoding = "utf-8"
    try:
        resp = r.json()["message"]
        await _send_message("wukong: %s" % (resp), event, message)
    except Exception as e:
        qqbot.logger.error(e) 
    return True

@command("/echo")
async def echo(param: str, event: str, message: qqbot.Message):
    if param.strip() == '':
        await _send_message("wukong: 请在指令后附上内容。例如 /echo 你是最棒的", event, message)
        return True
    await _chat(message.content.replace('/', '', 1), event, message)
    return True

async def _message_handler(event: str, message: qqbot.Message):
    """
    定义事件回调的处理
    :param event: 事件类型
    :param message: 事件对象（如监听消息是Message对象）
    """    
    qqbot.logger.info("event %s, receive message %s, from %s" % (event, message.content, message.author.id))

    tasks = [
        ask_menu, 
        play_music,
        echo,
        my_id,
        switch_on_do_not_bother,
        switch_off_do_not_bother
    ]
    for task in tasks:
        if await task("", event, message):
            return
    await _chat(message.content.replace('/', '', 1), event, message)

def run():
    """
    启动机器人
    """    
    # @机器人后推送被动消息
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    # 私信消息
    qqbot_direct_handler = qqbot.Handler(
        qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _message_handler
    )
    qqbot.async_listen_events(T_TOKEN, False, qqbot_handler, qqbot_direct_handler)

if __name__ == "__main__":
    run()