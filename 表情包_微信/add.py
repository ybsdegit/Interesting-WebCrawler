#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/10 20:15
# @Author  : Paulson
# @File    : add.py
# @Software: PyCharm
# @define  : function

with open('add.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if len(line) < 10:
            continue
        print(line.strip())