#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/7 23:40
# @Author  : Paulson
# @File    : NoverSpider.py
# @Software: PyCharm
# @define  : function
import requests


class NovelSpider:
    
    def __init__(self):
        self.session = requests.Session()
        
    def get_novel(self, url):
        index_html = self.download(url, encoding='gbk')
        print(index_html)
        
    def download(self, url, encoding):
        res = self.session.get(url)
        res.encoding = encoding
        return res.text
    
if __name__ == '__main__':
    
    nover_url = 'http://www.quanshuwang.com/book/9055'
    spider = NovelSpider()
    spider.get_novel(nover_url)
        
        
    