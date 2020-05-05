#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/7 20:59
# @Author  : Paulson
# @File    : analize.py
# @Software: PyCharm
# @define  : function
import pandas as pd

df = pd.read_csv('NeZha.csv', encoding='utf-8')
print(df.head())
print(df.info())

gender = df['gender']
print(gender)