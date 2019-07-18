#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 20:57
# @Author  : Paulson
# @File    : spider.py
# @Software: PyCharm
# @define  : function

import re
import json
from parse_url import parse_url
url = 'https://36kr.com/'
html_str = parse_url(url)
ret = re.findall('<script>window.initialState=(.*?)</script>', html_str)[0]
# print(ret)
ret = json.loads(ret)
with open('36kr.json', 'w', encoding='utf-8') as f:
    json.dump(ret, f, ensure_ascii=False, indent=2)
print(ret)