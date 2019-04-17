#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 20:12
# @Author  : Paulson
# @File    : qunar.py
# @Software: PyCharm
# @define  : function

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
1. 数据采集
"""

class Spider(object):
    """

    """
    def __init__(self, city, page):
        self.city = city
        self.page = page

    def get_urls(self):
        # https://travel.qunar.com/p-cs299878-shanghai-jingdian
        return ['https://travel.qunar.com/p-cs299878-{}-jingdian-1-'.format(self.city) + str(i) for i in range(1, self.page)]

    def get_infos(self, url):
        response = requests.get(url)
        soup_i = BeautifulSoup(response.text, 'lxml')
        info_items = soup_i.find('ul', class_="list_item clrfix").find_all('li')

        data = []
        for i in info_items:
            dic = {}
            dic['lat'] = i['data-lat']
            dic['lng'] = i['data-lng']
            dic['景点名称'] = i.find('span', class_="cn_tit").text
            dic['攻略提到数量'] = i.find('div', class_="strategy_sum").text
            dic['点评数量'] = i.find('div', class_="comment_sum").text
            dic['景点排名'] = i.find('span', class_="sum").text
            dic['星级'] = i.find('span', class_="total_star").find('span')['style'].split(':')[1]
            data.append(dic)
        return data

    def info_parse(self):
        df = pd.DataFrame()
        for url in self.get_urls():
            dfi = pd.DataFrame(self.get_infos(url))
            df = pd.concat([df, dfi])
            df.reset_index(inplace=True, drop=True)

        # df = pd.DataFrame()
        # for u in url_lst:
        #     dfi = pd.DataFrame(get_informations(u))
        #     df = pd.concat([df, dfi])
        #     df.reset_index(inplace=True, drop=True)
        #     # 采集数据
        df['lng'] = df['lng'].astype(np.float)
        df['lat'] = df['lat'].astype(np.float)
        df['点评数量'] = df['点评数量'].astype(np.int)
        df['攻略提到数量'] = df['攻略提到数量'].astype(np.int)
        # 字段类型处理

        df['星级'] = df['星级'].str.replace('%', '').astype(np.float)
        # 星级字段处理

        df['景点排名'] = df['景点排名'].str.replace('%', '').astype(np.int)

        '''
        3、景点筛选机制及评价方法
        '''
        print(df)

        self.zdnor(df, '攻略提到数量')
        self.zdnor(df, '星级')
        self.zdnor(df, '点评数量')

        df.to_excel('C:/Users/ybsde/Desktop/result.xlsx')
        return df

    def zdnor(self, dfi, col):
        dfi[col +  '-nor'] = (dfi[col] - dfi[col].min())/(dfi[col].max() - dfi[col].min())




s = Spider('shanghai', 20)
s.info_parse()
# s.data_plot('点评数量')
# for url in s.get_urls():
    # s.get_infos(url)

