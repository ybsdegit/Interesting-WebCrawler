#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 20:44
# @Author  : Paulson
# @File    : houlang.py
# @Software: PyCharm
# @define  : function
# https://api.bilibili.com/x/v1/dm/list.so?oid=186803402

import re
import requests
import csv


# 目标网址
url = "https://api.bilibili.com/x/v1/dm/list.so?oid=186803402"

# 请求
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}

res = requests.get(url, headers=headers)
html_doc = res.content.decode("utf-8")

# 解析
rule = re.compile('<d.*?">(.*?)</d>')
danmu = re.findall(rule, html_doc)
print(danmu)


# 保存
for line in danmu:
    with open('后浪弹幕.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        danmu = []
        danmu.append(line)
        writer.writerow(danmu)
