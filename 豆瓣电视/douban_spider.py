#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 21:31
# @Author  : Paulson
# @File    : douban_spider.py
# @Software: PyCharm
# @define  : function
import json

import requests

url = 'https://m.douban.com/rexxar/api/v2/subject_collection/tv_domestic/items?&start=0&count=18&loc_id=108288'


class DoubanSpider():
    def __init__(self):
        # self.url_temp = 'https://m.douban.com/rexxar/api/v2/subject_collection/tv_domestic/items?&start={}&count=18&loc_id=108288'
        self.num = 0
        self.url_temp = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=recommend&page_limit=20&page_start={}'
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
        }
    
    def parse_url(self, url):
        session = requests.session()
        session.get('https://m.douban.com/tv/chinese')
        # session.get('https://m.douban.com/j/to_app?url=https%3A%2F%2Fm.douban.com%2Ftv%2Fchinese&source=m_ad_nav&copy_open=1')
        response = session.get(url, headers=self.headers)
        return response.content.decode()
    
    def get_content_list(self, json_str):
        dict_ret = json.loads(json_str)
        content_list = dict_ret['subjects']
        return content_list
        
    def save_content_list(self, content_list):
        with open("douban.txt", 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write('\n')  # 写入换行符
    
    def run(self):
        
        """主要逻辑"""
        # 1. start_url
        url = self.url_temp.format(self.num)
        
        # 2. 发送请求，获取响应
        response = self.parse_url(url)
        # print(response)
        
        # 3. 提取数据
        content_list = self.get_content_list(response)
        print(content_list)
        
        # 4. 保存
        self.save_content_list(content_list)
        
        # 5. 构造下一页的url请求，进入循环
        if len(content_list) == 20:
            self.num += 20
            print("开始爬取{}-{}页数据".format(self.num, self.num+20))
            self.run()
        
        
if __name__ == '__main__':
    douban = DoubanSpider()
    douban.run()
