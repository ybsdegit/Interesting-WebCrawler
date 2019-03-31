#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/30 21:25
# @Author  : Paulson
# @File    : data_analysis.py
# @Software: PyCharm
# @define  : function

from pyecharts import Bar
import pandas as pd
import numpy as np
import seaborn as sns
import collections
import matplotlib.pyplot as plt
from pymongo import MongoClient
from pandas.io.json import json_normalize
plt.style.use('ggplot')
from  pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']   # 解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))  # 把plt默认的图片size调大一点
plt.rcParams['figure.dpi'] = mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像显示'-'显示为方块的问题
conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('Lianjia')  # 连接到Lianjia数据库

zufang = db.get_collection('zufang')  # 连接到集合zufang
mon_data = zufang.find()  # 查询这个集合下的所有记录
data = json_normalize([comment for comment in mon_data])
print(data.head())
print(data.info())

# 每个城市各采样3000条数据，保存为csv文件
# data_sample = pd.concat([data[data['city'] == city].sample(3000) for city in ['北京', '上海', '广州']])
# data_sample.to_csv('data_sample.csv', index=False)

# 数据清洗
# 1. 去掉 _id
data = data.drop(columns='_id')

# 2. bathroom_num
data['bathroom_num'].unique()
print(data['bathroom_num'].unique())

print(data[data['bathroom_num'].isin(['8', '9', '10'])])

# data['rent_price_listing'].apply(get_aver)

def get_city_zf_loc(city, city_short, col=['longitude', 'latitude', 'dist'], data=data):
    file_name = 'data_' + city_short + '_latlon.csv'
    data_latlon = data.loc[data['city'] == city, col].dropna(subset=['latitude', 'longitude'])
    data_latlon['longitude'] = data_latlon['longitude'].astype(str)
    data_latlon['latitude'] = data_latlon['latitude'].astype(str)
    data_latlon['latlon'] = data_latlon['longitude'].str.cat(data_latlon['latitude'], sep=',')
    data_latlon.to_csv(file_name, index=False)
    print(city + '的数据一共有{}条'.format(data_latlon.shape[0]))

get_city_zf_loc('北京', 'bj', ['longitude','latitude', 'dist'])
get_city_zf_loc('上海', 'sh', ['longitude','latitude', 'dist'])
get_city_zf_loc('广州', 'gz', ['longitude','latitude', 'dist'])
# get_city_zf_loc('深圳', 'sz', ['longitude','latitude', 'dist'])

fig = plt.figure(dpi=300)
data.dropna(subset=['latitude', 'longitude'])[data['city']=='北京']['dist'].value_counts(ascending=True).plot.barh()

from scipy import stats
from pyecharts import WordCloud
bj_tag = []
for st in data[data['city']=='北京'].dropna(subset=['house_tag'])['house_tag']:
    bj_tag.extend(st.split(' '))

name, value = WordCloud.cast(collections.Counter(bj_tag))
wordcloud = WordCloud(width=500, height=500)
wordcloud.add("", name, value, word_size_range=[20, 100])
print(wordcloud)