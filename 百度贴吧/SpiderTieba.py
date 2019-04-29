#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/27 20:37
# @Author  : Paulson
# @File    : SpiderTieba.py
# @Software: PyCharm
# @define  : function
import os

import requests
from lxml import etree


class Spider(object):
    """
    爬取百度贴吧数据
    """
    def __init__(self):
        # self.query_string = query_string
        self.url = "https://tieba.baidu.com/f?"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) '}   # 不能添加这一段，不然获取不到数据 Chrome/74.0.3729.108 Safari/537.36


    def params(self):
        para = {
            "kw": "女神"
        }
        return para

    def send_request(self, url, parms={}):
        """
        1. 发送请求
        :param url:
        :param param:
        :return:
        """
        response = requests.get(url, params=parms, headers=self.headers)
        # s = response.url
        # print(s)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(str(response.content.decode()))
        return response.content

    def parse_data(self, data, rule):
        """
        2. 数据清洗
        :return:
        """
        html_data = etree.HTML(data)
        data_list = html_data.xpath(rule)
        return data_list

    def sava_data(self, data, image_name):
        """
        3. 保存数据
        :return:
        """
        os.makedirs('./images/', exist_ok=True)
        image_path = 'images/' + image_name
        with open(image_path, 'wb') as f:
            print('正在爬取: ', image_name)
            f.write(data)


    def run(self):
        """
        main逻辑
        :return:
        """
        tieba_params = self.params()
        datas = self.send_request(self.url, tieba_params)
        detail_rule = '//div[@class="t_con cleafix"]/div/div/div/a/@href'
        url_list = self.parse_data(datas, detail_rule)

        for lable in url_list:
            url = 'http://tieba.baidu.com' + lable
            detail_data = self.send_request(url)

            # 解析图片url
            image_url_rule = '//img[@class="BDE_Image"]/@src'
            image_url_list = self.parse_data(detail_data, image_url_rule)

            # 列表切片去图片名字
            for image_url_l in image_url_list:
                image_data = self.send_request(image_url_l)
                image_name = image_url_l[-12:]
                self.sava_data(image_data, image_name)


if __name__ == '__main__':
    # s_search = input("请输入查询关键字")
    tei_ba = Spider()
    tei_ba.run()
