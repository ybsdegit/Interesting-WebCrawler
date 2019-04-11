#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/31 15:25
# @Author  : Paulson
# @File    : comment_crawler.py
# @Software: PyCharm
# @define  : function
import random
from datetime import datetime
import time
import pymongo
import requests
from requests.exceptions import *
from Wandering_Earth import cookies
'''

'''
class Spider:
    """
    猫眼电影：流浪地球，爬取评论信息
    """
    def __init__(self):
        self.movieId = 24890
        self.offset = 0
        self.limit = 15
        self.setting_mongo()
        self.time = int(time.time() * 1000)  # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）* 1000
        self.premiere_time = int(time.mktime(time.strptime('2019-02-05 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000)

    def get_comment(self):
        """
        爬取首映到当前时间的电影评论
        :return: None
        url: 评论真实请求的url，参数ts为时间戳
        """
        # url = 'http://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&' \
        #       'offset=0&limit=15&ts={}&type=3'
        # url = 'http://m.maoyan.com/review/v2/comments.json?movieId={}&userId=-1&offset={}&limit={}&ts={}&type=3'
        url = 'http://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&' \
              'offset=0&limit=15&ts={}&type=3'
        while self.time > self.premiere_time:
            req_url = url.format(self.time)

            # req_url = url.format(self.movieId,self.offset,self.limit,self.time)
            print(req_url)
            try:
                res = requests.get(req_url, headers=self.get_headers())
                count = 0
                print(res.json())
                comments = res.json()['data']['comments']
                for com in comments:
                    self.parse_comment(com=com)
                    count += 1
                    if count == 10:
                        self.time = com['time']
                        print(self.time)
                print('成功爬取截止到{}的数据！'.format(datetime.fromtimestamp(int(self.time/1000))))
            except KeyError:
                raise
            except Exception as e:
                print(e)
                raise

    def parse_comment(self, com):
        """
        解析函数，用来解析爬回来的json评论数据，并把数据保存到MongoDB数据库
        :param com: 每一条评论的json数据
        :return: None
        """
        # 构造评论字典
        comment = {
            'content': com['content'],
            'gender': com['gender'],
            'id': com['id'],
            'nick': com['nick'],
            'replyCount': com['replyCount'],
            'score': com['score'],
            'userId': com['userId'],
            'userLevel': com['userLevel'],
        }
        # 通过评论id去重，如果有了就更新，没有就插入
        self.db['maoyan'].update_one({'id': comment['id']}, {'$set': comment}, upsert=True)

    def main(self, page):
        pass


    def get_headers(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)\ AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Connection': 'keep-alive',
            'Cookie': '_lxsdk_cuid=169d2a42f25c8-04e8e5d83cca73-7a1437-1fa400-169d2a42f25c8; uuid_n_v=v1; iuuid=5AEB9630538711E9BF7E2751D1FC5709AA0ABC3224EA4E4DB3735E72F6E50C3E; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; _lxsdk=4078EA60538611E982F8D140B60ED647FF8874FFE91344AB891BBA74CD05B123; __mta=20795911.1554017169428.1554017232388.1554019098435.5'
        }
        return headers

    def setting_mongo(self):
        """
        设置MongoDB数据库
        :return: None
        """
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['MaoYan']
        self.db['maoyan'].create_index('id', unique=True)  # 评论的id为主键进行去重


if __name__ == '__main__':
    my = Spider()
    my.get_comment()
