#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 21:53
# @Author  : Paulson
# @File    : 大碗宽面.py
# @Software: PyCharm
# @define  : function
import random
import time

import jieba
import requests
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import numpy as np
import PIL.Image as Image
class Spider(object):
    def __init__(self):
        self.hot_url = "http://music.163.com/api/v1/resource/comments/R_SO_4_1359595520?limit=20&offset=0"
        self.all_url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_1359595520?limit=20&offset={}'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}

    def get_data(self,url):
        return requests.get(url, headers=self.headers).json()

    def parse_data_hot(self):
        data = self.get_data(self.hot_url)
        hotComments = data['hotComments']
        contentlist = []
        for i in hotComments:
            content = i['content']
            contentlist.append(content)
        return contentlist

    def parse_data_all(self):
        all_comments = []  # 提取前100页评论信息
        for j in range(0, 2001, 20):
            all_url = self.all_url.format(j)
            for k in range(0, 20):
                data = self.get_data(all_url)
                comment = data['comments'][k]['content']  # 所有评论
                all_comments.append(comment)
            print('正在抓取全部评论，请稍等...')
            time.sleep(int(format(random.randint(3, 6))))
        return all_comments

    def all_wc(self):
        content_all_list = self.parse_data_all()
        text = ' '.join(content_all_list)
        cut = jieba.cut(text, cut_all=True)
        word = ','.join(cut)
        coloring = np.array(Image.open("1.jpg"))  # 电脑中自定义词云的图片
        my_wordcloud = WordCloud(background_color="white", max_words=3000, max_font_size=200,
                                 mask=coloring, random_state=100, font_path='simsun.ttc',
                                 scale=3).generate(word)  # 定义词云背景图颜色、尺寸、字体大小、电脑中字体选择,random_state 为每个单词返回一个PIL颜色
        image_colors = ImageColorGenerator(coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 绘图颜色
        plt.imshow(my_wordcloud)  # 绘图内容
        plt.axis("off")
        # plt.show()  # 显示图
        # d = path.dirname(__file__)  # project 当前目录
        # my_wordcloud.to_file(path.join(d, '热门评论图.png'))
        my_wordcloud.to_file("全部评论图.jpg")
        print('全部评论词云图完成，在项目代码目录下查看')


    def hot_wc(self):
        content_list = self.parse_data_hot()
        text = ' '.join(content_list)
        cut = jieba.cut(text, cut_all=True)
        word = ','.join(cut)
        coloring = np.array(Image.open("1.jpg"))  # 电脑中自定义词云的图片
        my_wordcloud = WordCloud(background_color="white", max_words=3000, max_font_size=200,
                                 mask=coloring, random_state=100, font_path='simsun.ttc',
                                 scale=3).generate(word)  # 定义词云背景图颜色、尺寸、字体大小、电脑中字体选择,random_state 为每个单词返回一个PIL颜色
        image_colors = ImageColorGenerator(coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))  # 绘图颜色
        plt.imshow(my_wordcloud)  # 绘图内容
        plt.axis("off")
        # plt.show()  # 显示图
        # d = path.dirname(__file__)  # project 当前目录
        # my_wordcloud.to_file(path.join(d, '热门评论图.png'))
        my_wordcloud.to_file("热门评论图.jpg")
        print('热门评论词云图完成，在项目代码目录下查看')



if __name__ == '__main__':
    s = Spider()
    s.hot_wc()
    s.all_wc()