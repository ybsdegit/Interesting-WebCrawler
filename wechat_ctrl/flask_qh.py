#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 23:52
# @Author  : Paulson
# @File    : flask_qh.py
# @Software: PyCharm
# @define  : function
from random import choice

from flask import Flask

app = Flask(__name__)
content_list = []

def get_message_girlfriend():
    global content_list
    if content_list:
        return choice(content_list)
    with open('honeyed.txt', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        for content in contents:
            content_list.append(content)
    return choice(content_list)

@app.route('/')
def hello_world():
    message = get_message_girlfriend()
    return message


if __name__ == '__main__':
    app.run()