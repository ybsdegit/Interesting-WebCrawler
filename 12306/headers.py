#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 23:39
# @Author  : Paulson
# @File    : headers.py
# @Software: PyCharm
# @define  : function

import re

headers_str = """answer: 34,34,38,105
rand: sjrand
login_site: E"""
pattern = '^(.*?): (.*)$'

for line in headers_str.splitlines():
    print(re.sub(pattern,'\'\\1\':\'\\2\',', line))