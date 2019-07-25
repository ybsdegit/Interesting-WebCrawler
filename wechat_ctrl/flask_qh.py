#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 23:52
# @Author  : Paulson
# @File    : flask_qh.py
# @Software: PyCharm
# @define  : function
import random

from flask import Flask

app = Flask(__name__)

def get_message_girlfriend():
    content_list = []
    with open('honeyed.txt', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        for content in contents:
            content_list.append(content)
    i = len(content_list)
    message = content_list[random.randint(0, i-1)]
    return message

@app.route('/')
def hello_world():
    message = get_message_girlfriend()
    return message


if __name__ == '__main__':
    app.run()