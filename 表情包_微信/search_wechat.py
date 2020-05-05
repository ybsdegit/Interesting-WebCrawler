#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/10 18:47
# @Author  : Paulson
# @File    : search_wechat.py
# @Software: PyCharm
# @define  : function
import glob
import time
import itchat
from itchat.content import TEXT, PICTURE
from random import choice


imgs = []
path = r'C:\Users\ybsde\PycharmProjects\Interesting-WebCrawler\表情包_微信\baoqingbao\*'
content_list = []
dear_list = ['宝哥', '亲爱的']


def get_message_girlfriend():
    global content_list
    if content_list:
        return choice(content_list)
    with open('honeyed.txt', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        for content in contents:
            content_list.append(content)
    return choice(content_list)


def search_image(text):
    print('收到关键字：', text)
    for name in glob.glob(path + text + '*.jpg'):
        imgs.append(name)
    for name in glob.glob(path + text + '*.gif'):
        imgs.append(name)


def get_choice(num: int) -> list:
    img_sends = []
    for i in range(num):
        img_sends.append(choice(imgs))
    return img_sends
    

@itchat.msg_register([PICTURE, TEXT])
def text_reply(msg):
    search_image(msg.text)
    dear_flag = [True for i in dear_list if i in msg.text]
    if dear_flag:
        honeyed = get_message_girlfriend()
        print('honeyed: ', honeyed)
        msg.user.send(honeyed)
    
    if not imgs:
        print(None)
        return 'None'
    img_sends = get_choice(1)
    for img in img_sends:
        print('开始发送表情: ', img)
        time.sleep(0.3)
        msg.user.send_image(img)
        time.sleep(0.3)
    imgs.clear()


itchat.auto_login(hotReload=True)
itchat.run()
