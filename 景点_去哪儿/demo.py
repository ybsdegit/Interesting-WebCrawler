#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/11 21:37
# @Author  : Paulson
# @File    : demo.py
# @Software: PyCharm
# @define  : function

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 17:48:21 2019

@author: iHJX_Alienware
"""

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('导入模块')

import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
# Matplotlib中设置字体-黑体，解决Matplotlib中文乱码问题
plt.rcParams['axes.unicode_minus'] = False
# 解决Matplotlib坐标轴负号'-'显示为方块的问题


'''
1、数据采集
'''


def get_urls(n):
    return ['https://travel.qunar.com/p-cs299878-shanghai-jingdian-1-' + str(i + 1) for i in range(n)]
    # 创建函数，获取分页网址


def get_informations(u):
    ri = requests.get(u)
    # requests访问网站
    soupi = BeautifulSoup(ri.text, 'lxml')
    # bs解析页面
    infori = soupi.find('ul', class_="list_item clrfix").find_all('li')
    # 获取列表内容

    datai = []
    n = 0
    for i in infori:
        n += 1
        # print(i.text)
        dic = {}
        dic['lat'] = i['data-lat']
        dic['lng'] = i['data-lng']
        dic['景点名称'] = i.find('span', class_="cn_tit").text
        dic['攻略提到数量'] = i.find('div', class_="strategy_sum").text
        dic['点评数量'] = i.find('div', class_="comment_sum").text
        dic['景点排名'] = i.find('span', class_="ranking_sum").text
        dic['星级'] = i.find('span', class_="total_star").find('span')['style'].split(':')[1]
        datai.append(dic)
        # 分别获取字段内容
        # print('已采集%s条数据' %(n*10))
    return datai

    # 构建页面爬虫


url_lst = get_urls(5)
# 获取5页网址

df = pd.DataFrame()
for u in url_lst:
    dfi = pd.DataFrame(get_informations(u))
    df = pd.concat([df, dfi])
    df.reset_index(inplace=True, drop=True)
    # 采集数据

'''
2、字段筛选与数据清洗
'''
df['lng'] = df['lng'].astype(np.float)
df['lat'] = df['lat'].astype(np.float)
df['点评数量'] = df['点评数量'].astype(np.int)
df['攻略提到数量'] = df['攻略提到数量'].astype(np.int)
# 字段类型处理

df['星级'] = df['星级'].str.replace('%', '').astype(np.float)
# 星级字段处理

df['景点排名'] = df['景点排名'].str.split('第').str[1]
df['景点排名'].fillna(value=0, inplace=True)

'''
3、景点筛选机制及评价方法
'''
import matplotlib.style as psl

psl.use('seaborn-colorblind')


def createfig(col):
    dffig = df[['景点名称', col]].sort_values(by=col, ascending=True).iloc[:10]
    dffig.index = dffig['景点名称']
    dffig.iloc[::-1].plot(kind='bar', rot=90,
                          title='%sTOP排名' % col, figsize=(12, 6))
    plt.grid()
    # 创建函数绘制TOP10的对应指标图片

createfig('点评数量')




