#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 20:45
# @Author  : Paulson
# @File    : wechat_ctrl.py
# @Software: PyCharm
# @define  : function
import random
from ctypes import windll
import itchat


def get_message_girlfriend():
    content_list = []
    with open('honeyed.txt', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        for content in contents:
            content_list.append(content)
    i = len(content_list)
    message = content_list[random.randint(0, i-1)]
    return message

# 消息注册机制
# 只要接受到的任何的文本消息，就自动调用下方的函数

@itchat.msg_register(['Text'])
def message(msg):
    print(msg)
    data = msg['Text'].strip()
    ToUserName = msg['ToUserName']
    FromUserName = msg['FromUserName']
    UserName = msg['User']['UserName']
    
    
    try:
        NickName = msg['User']['NickName']
    except:
        NickName = 'self'
    print(NickName + ': ' + data)
    message_girlfriend = get_message_girlfriend()
    NickNames = ['choudashouzb', '安心睡觉', 'SinoSky']

    # 如果是自己发的消息，就不回复了
    FromUserName_Me = '@35ab3129cbf98b03105ebbfbc2a9c5e20fa419e5d4437a979fe726b0dcc217da'
    if FromUserName != FromUserName_Me:
        if NickName in NickNames:
            print('发一段话')
            print(message_girlfriend, UserName)
            itchat.send(message_girlfriend, UserName)
            
    if FromUserName == ToUserName:
        itchat.send(message_girlfriend, 'filehelper')
 
    # 取出发给文件助手的消息
    if ToUserName == 'filehelper':
        if data == '锁屏':
            user32 = windll.LoadLibrary('user32.dll')
            user32.LockWorkStation()
        
        
def main():
    
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == '__main__':
    main()