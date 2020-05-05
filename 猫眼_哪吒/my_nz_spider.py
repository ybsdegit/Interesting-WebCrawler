#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/7 20:38
# @Author  : Paulson
# @File    : my_nz_spider.py
# @Software: PyCharm
# @define  : function
import csv
import json
from pymongo import MongoClient
import requests
import pandas as pd

client = MongoClient()
db = client['maoyao']['NeZha']

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36'
}

def get_json_data(url):
    response_data = requests.get(url, headers=headers).json()
    print(response_data)
    return response_data
    
def save_date(content_list):
    keys = content_list[0].keys()
    values = [i.values() for i in content_list]
    print(keys)
    print(values)
    
    with open('NeZha.csv', 'a', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(keys)
        for i, v in enumerate(values):
            csv_writer.writerow(values[i])
    
        
    print('*'*10 + '保存成功' +'*'*10)

def save_db_mongo(item):
    db.insert(item)
    print('*'*10 + 'Mongo保存成功' +'*'*10)


def parse_json(data):
    content_list = []
    comments = data['data']['comments']
    for comment in comments:
        # print(comments)
        com_content = {}
        com_content['gender'] = comment['gender']  # 性别 1 男 2 女
        com_content['score'] = comment['score']  # 评分
        com_content['content'] = comment['content']  # 评论内容
        com_content['upCount'] = comment['upCount']  # 点赞
        com_content['userLevel'] = comment['userLevel']  # 用户等级
        print(com_content)
        content_list.append(com_content)
        save_db_mongo(com_content)
        
    return content_list
    


if __name__ == '__main__':
    num = 0
    error = 0
   
    while True:
        try:
            url = 'http://m.maoyan.com/review/v2/comments.json?movieId=1211270&userId=-1&offset={}&limit=15&ts=0&type=3'.format(num)
            data = get_json_data(url)
            content_list = parse_json(data)
            save_date(content_list)
            num += 15
        except:
            error += 1
            if error == 15:
                print('爬取结束')
                break
                