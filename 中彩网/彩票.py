#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/30 20:42
# @Author  : Paulson
# @File    : 彩票.py
# @Software: PyCharm
# @define  : function
import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'Referer':'http://kaijiang.zhcw.com/zhcw/html/3d/list.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

def get_table(url):
    """
    获取表格数据
    :param url:
    :return:
    """
    res = requests.get(url, headers=headers).text
    soup = BeautifulSoup(res, 'lxml')
    content = soup.select('.wqhgt')[0]
    tbl = pd.read_html(content.prettify(), header=1)[0]
    df1 = pd.DataFrame(tbl)
    x, y = df1.shape
    df1 = df1.drop([x - 1])
    # df.update(df1)
    # df.append(df1, ignore_index=True)
    return df1

if __name__ == '__main__':
    df_table_list = pd.DataFrame()
    url = 'http://kaijiang.zhcw.com/zhcw/html/3d/list.html'
    url1 = 'http://kaijiang.zhcw.com/zhcw/html/3d/list_2.html'
    # df_table = get_table(url)
    for i in range(0, 265):
        url = f'http://kaijiang.zhcw.com/zhcw/inc/3d/3d_wqhg.jsp?pageNum={i}'
        print(url)
        df_table = get_table(url)
        df_table_list = pd.concat([df_table_list, df_table], ignore_index=True)
    # pass