#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 21:33
# @Author  : Paulson
# @File    : 大碗宽面Analysis.py
# @Software: PyCharm
# @define  : function

from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import pandas as pd
import jieba

df = pd.read_csv('noodles.csv', header=None)

text = ''
for line in df[1]:
    text += ' '.join(jieba.cut(line, cut_all=False))

backgroud_Image = plt.imread('kris.png')

wc = WordCloud(background_color='black', font_path='simsun.ttc',
               max_words=2000, max_font_size=50, random_state=50,)

wc.generate_from_text(text)

# 看看词频高的有哪些,把无用信息去除
process_word = WordCloud.process_text(wc, text)
sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
print(sort[:50])
# img_colors = ImageColorGenerator(backgroud_Image)
# wc.recolor(color_func=img_colors)
plt.imshow(wc)
plt.axis('off')
wc.to_file("wyfciyun.jpg")
print('生成词云成功!')