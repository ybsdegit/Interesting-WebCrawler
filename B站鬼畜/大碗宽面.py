#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 21:06
# @Author  : Paulson
# @File    : 大碗宽面.py
# @Software: PyCharm
# @define  : function
import requests
from bs4 import BeautifulSoup
import pandas as pd

class Spider(object):

    def __init__(self):
        self.url = "http://comment.bilibili.com/87150521.xml"

    def get_html(self):
        html = requests.get(self.url).content.decode('utf-8')
        return html


    def parse_xml(self):
        html_data = self.get_html()
        soup = BeautifulSoup(html_data, 'lxml')
        results = soup.find_all('d')

        comments = [comment.text for comment in results]
        comment_dict = {'comments': comments}

        df = pd.DataFrame(comment_dict)
        df.to_csv('noodles.csv', encoding='utf-8')


if __name__ == '__main__':
   s = Spider()
   s.parse_xml()