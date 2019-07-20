#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 20:50
# @Author  : Paulson
# @File    : qiushi.py
# @Software: PyCharm
# @define  : function
import time

import requests
from lxml import etree
import pyttsx3

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.90 Safari/537.36'
}


def parse_url(url):
    """解析url"""
    try:
        return requests.get(url, headers=headers, timeout=10).text
    except TimeoutError as msg:
        print('爬取异常'+str(msg))

def get_parse_info(response, patten):
    """解析网页"""
    html = etree.HTML(response)
    info = html.xpath(patten)
    return info


def save_file(file_name, content):
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(','.join(content))
        f.write('\n')


def read_content(content):
    """语音读文本"""
    engine = pyttsx3.init()
    engine.say(content)
    engine.runAndWait()

def get_last_info(detail_url):
    detail_response = parse_url(detail_url)
    detail_content = get_parse_info(detail_response, patten='//div[@class="content"]/text()')
    return detail_content


def run():
    start = time.time()
    num = 1
    # start_url = 'https://www.qiushibaike.com/text/'
    # url = 'https://www.qiushibaike.com/text/page/{}/'.format(num)
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(num) for num in range(1, 51)]
    
    for url in urls:
        response = parse_url(url)
        list_info = get_parse_info(response, patten='//a[@class="contentHerf"]/@href')
        list_urls = ['https://www.qiushibaike.com' + str(info) for info in list_info]
    
        for detail_url in list_urls:
            detail_content = get_last_info(detail_url)
            print(detail_content)
            save_file('qiushi.txt', detail_content)
    end = time.time()
    print('Cost time:', end - start)
    
    
   
    # new_list_info = []
    # for new_url in list_info:
    #     new_list_info.append(old_url+str(new_url))


if __name__ == '__main__':
    run()
