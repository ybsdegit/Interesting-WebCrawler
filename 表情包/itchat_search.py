#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 0:56
# @Author  : Paulson
# @File    : itchat_search.py
# @Software: PyCharm
# @define  : function
import time

import itchat
# itchat.auto_login(hotReload=True)

@itchat.msg_register(itchat.content.TEXT)
def reply_msg(msg):
    print("收到一条信息：",msg.text)

if __name__ == '__main__':
    itchat.auto_login()
    time.sleep(5)
    itchat.send("文件助手你好哦", toUserName="filehelper")
    itchat.run()