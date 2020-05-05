#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 21:06
# @Author  : Paulson
# @File    : show_data.py
# @Software: PyCharm
# @define  : function

import jieba
import wordcloud


with open('后浪弹幕.csv', encoding='utf-8') as f:
    txt = f.read()
    
txt_list = jieba.lcut(txt)
txt_str = ' '.join(txt_list)
print(txt_str)

w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='msyh.ttc',
                        scale=15,
                        stopwords={' '},
                        contour_color='red',
                        contour_width='5'
                        )
w.generate(txt_str)
w.to_file('后浪弹幕.jpg')