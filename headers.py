#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 23:39
# @Author  : Paulson
# @File    : headers.py
# @Software: PyCharm
# @define  : function

import re

# headers_str =''

with open('headers.txt', 'r', encoding='utf-8') as f:
    headers_str = f.read()

pattern = '^(.*?): (.*)$'
for line in headers_str.splitlines():
    print(re.sub(pattern,'\'\\1\':\'\\2\',', line))