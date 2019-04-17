#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 23:32
# @Author  : Paulson
# @File    : 无名之辈.py
# @Software: PyCharm
# @define  : function
import json

import requests


def getMoveinfo(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
    }
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parseInfo(html):
    data = json.loads(html)['cmts']
    for item in data:
        print(item)
        yield{
            'date':item['startTime'],
            'nickname':item['nickName'],
            'city':item['cityName'],
            'rate':item['score'],
            'conment':item['content']
        }

if __name__ == '__main__':
    url = "http://m.maoyan.com/mmdb/comments/movie/1208282.json?v=yes&offset=15"
    html = getMoveinfo(url)
    parseInfo(html)
