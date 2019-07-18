#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 20:58
# @Author  : Paulson
# @File    : parse_url.py
# @Software: PyCharm
# @define  : function

import requests

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}

def parse_url(url):
    return requests.get(url, headers=headers).text