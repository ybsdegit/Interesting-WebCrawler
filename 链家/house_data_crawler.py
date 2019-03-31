#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/29 21:22
# @Author  : Paulson
# @File    : house_data_crawler.py
# @Software: PyCharm
# @define  : function
import re
import time

import requests

from 链家.info import rent_type, city_info
from requests.exceptions import ConnectionError
# from pymongo import MongoClient
import pymongo


class Rent(object):
    """
        初始化函数，获取租房类型（整租，合租），要爬取的城市分区信息以及连接MongoDB数据库

    """

    def __init__(self):
        self.rent_type = rent_type
        self.city_info = city_info

        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['Lianjia']
        self.db['zufang'].create_index('m_url', unique=True)  # 以m端连接为主键进行去重
        # self.proxies = self.db['proxies']
        # self.proxies.ensure_index('proxy', unique=True)

    def get_data(self):
        """
         爬取不同租房类型、不同城市各区域的租房信息
        :return: None
        """
        for ty, type_code in self.rent_type.items():   # 整租，合租
            for city, info in self.city_info.items():  # 城市、城市各区域信息
                for dist, dist_py in info[2].items():  # 各区域及其拼音
                    fir_url = 'https://m.lianjia.com/chuzu/{}/zufang/{}/'.format(info[1], dist_py)
                    rec_bc = requests.get(fir_url)     # url = 'https://m.lianjia.com/chuzu/bj/zufang/dongcheng/
                    # print(url)
                    # print(rec_bc.text)
                    pa_bc = r"data-type=\"bizcircle\" data-key=\"(.*)\" class=\"oneline \">"
                    bc_list = re.findall(pa_bc, rec_bc.text)  # 商圈
                    self._writer_bc(bc_list)
                    bc_list = self._read_bc()  # 先爬取各区的商圈，最终以各区商圈来爬数据，如果按区爬，每区最多只能获得2000条数据
                    print(bc_list)

                    if len(bc_list) > 0:
                        for bc_name in bc_list:
                            idx = 0
                            has_more = 1

                            while has_more:
                                try:
                                    url = 'https://app.api.lianjia.com/Rentplat/v1/house/list?city_id={}&condition={}' \
                                          '/rt{}&limit=30&offset={}&request_ts={}&scene=list'.format(info[0],
                                                                                                     bc_name,
                                                                                                     type_code,
                                                                                                     idx*30,
                                                                                                     int(time.time()))
                                    print(url)
                                    res = requests.get(url=url, timeout=10)
                                    print(res.text)
                                    # city 城市 dist:区 bc_name：
                                    print('成功爬取 {} 市 {}-{} 的 {} 第 {} 页数据'.format(city, dist, bc_name, ty, idx+1))
                                    item = {'city': city, 'type': ty, 'dist': dist}
                                    print(item)
                                    self._parse_record(res.json()['data']['list'], item)
                                    total = res.json()['data']['total']
                                    idx += 1
                                    if total/30 <= idx:
                                        has_more = 0
                                except ConnectionError:
                                    print('链接访问不成功，正在重试！')

    def _parse_record(self, data, item):
        """
        解析函数，用于解析爬回来的response的json数据
        :param data: 一个包含房源数据的列表
        :param item: 传递字典
        :return: None
        """
        if len(data) > 0:
            for rec in data:
                item['bedroom_num'] = rec['frame_bedroom_num']  # 床位
                item['hall_num'] = rec['frame_hall_num']
                item['bathroom_num'] = rec['frame_bathroom_num']
                item['rent_type'] = rec['rent_type']
                item['house_title'] = rec['house_title']
                item['resblock_name'] = rec['resblock_name']
                item['bizcircle_name'] = rec['bizcircle_name']
                item['layout'] = rec['layout']
                item['rent_price_listing'] = rec['rent_price_listing']
                item['house_tag'] = self._parse_house_tags(rec.get('house_tags'))
                item['m_url'] = rec['m_url']
                item['rent_price_unit'] = rec['rent_price_unit']

                try:
                    res2 = requests.get(item['m_url'], timeout=5)
                    pa_lon = r"longitude: '(.*)',"
                    pa_lat = r"latitude: '(.*)'"
                    pa_distance = r"<span class=\"fr\">(\d*)米</span>"
                    item['longitude'] = re.findall(pa_lon, res2.text)[0]
                    item['latitude'] = re.findall(pa_lat, res2.text)[0]
                    distance = re.findall(pa_distance, res2.text)

                    if len(distance) > 0:
                        item['distance'] = distance[0]
                    else:
                        item['distance'] = None

                except ConnectionError:
                    item['longitude'] = None
                    item['latitude'] = None
                    item['distance'] = None
                    print('访问m链接错误')

                self.db['zufang'].update_one({'m_url': item['m_url']}, {'$set': item}, upsert=True)
                print('成功保存数据： {}！'.format(item))

    @staticmethod
    def _parse_house_tags(house_tag):
        """
        处理 house_tag 字段，相当于数据清洗
        :param house_tag: house_tags 字段的数据
        :return: 处理后的house_tags
        """
        if len(house_tag) > 0:
            st = ''
            for tag in house_tag:
                st += tag.get('name') + ' '
            return st.strip()

    @staticmethod
    def _writer_bc(bc_list):
        """
        把爬取的商圈写入txt，为了整个爬取的过程更加可控
        param bc_list: 商圈list
        :return: None
        """

        with open('bc_list.txt', 'w') as f:
            for bc in bc_list:
                f.write(bc+'\n')

    @staticmethod
    def _read_bc():
        """
          读入商圈
        :return: list
        """
      
        with open('bc_list.txt', 'r') as f:
            return [bc.strip() for bc in f.readlines()]


if __name__ == '__main__':
    r = Rent()
    r.get_data()
