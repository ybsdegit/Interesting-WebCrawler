#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/31 15:25
# @Author  : Paulson
# @File    : comment_crawler.py
# @Software: PyCharm
# @define  : function
import random
import re
from datetime import datetime
import time
import pymongo
import requests
from requests.exceptions import *
from Wandering_Earth import cookies
from fake_useragent import UserAgent
import logging

logging.basicConfig(level=logging.INFO,#控制台打印的日志级别
                    filename='maoyan.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s' #日志格式
                    )

class Spider:
    """
    猫眼电影：流浪地球，爬取评论信息
    """
    def __init__(self):
        # 每次抓取评论数，猫眼最大支持30
        self.limit = 30
        # 流浪地球
        self.movieId = '248906'
        self.ts = 0
        self.count = 0
        self.offset = 0
        self.setting_mongo()
        self.ua = UserAgent(verify_ssl=False)
        self.time = int(time.time() * 1000)  # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）* 1000
        self.premiere_time = int(time.mktime(time.strptime('2019-02-05 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000)



    def get_url(self):
        url = 'http://m.maoyan.com/review/v2/comments.json?movieId=' + self.movieId + '&userId=-1&offset=' + str(
            self.offset) + '&limit=' + str(self.limit) + '&ts=' + str(self.ts) + '&type=3'
        return url

    def open_url(self,url):
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(e)
            return None

    def parse_comments(self, data):
        ts_duration = self.ts
        comments = data['data']['comments']
        for com in comments:
            com_time = com['time']
            if self.ts == 0:
                ts = com_time
                ts_duration = com_time
            if self.ts != com_time and self.ts == ts_duration:
                ts_duration = com_time
            if com_time != ts_duration:
                self.ts = ts_duration
                self.offset = 0
                return self.get_url()
            else:
                content = re.sub("[\r\n|\r|\n|;]", "。",com['content'].strip())  # comment['content'].strip().replace('\n', '。')
                # content = re.sub("[\s+\.\!\/_,$%^*()+\"\'\?]+|[+——！，。？、~@#￥%……&*（）【】；：]+|\[.+\]|\［.+\］", "", comment['content'].strip())
                logging.info('get comment ' + str(self.count))
                self.count += 1


    def setting_mongo(self):
        """
        设置MongoDB数据库
        :return: None
        """
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['MaoYan']
        self.db['maoyan'].create_index('id', unique=True)  # 评论的id为主键进行去重


if __name__ == '__main__':
    logging.info('start get comment')
    my = Spider()
    url = my.get_url()
    while True:
        try:
            data = my.open_url(url)
            print(data)
            if data:
                url = my.parse_comments(data)
                if not url:
                    logging.info('end')
                    break
        except Exception as e:
            logging.exception('异常')
            time.sleep(random.random()*3)
