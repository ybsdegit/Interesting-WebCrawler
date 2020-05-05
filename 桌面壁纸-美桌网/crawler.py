#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 21:34
# @Author  : Paulson
# @File    : crawler.py
# @Software: PyCharm
# @define  : function

# url = 'http://pic1.win4000.com/wallpaper/2020-04-16/5e97eb67a4d25.jpg'
# ur1 = 'http://pic1.win4000.com/wallpaper/2020-04-16/5e97eb6f5f817_270_185.jpg'

import requests
import parsel
import os

# url
url = 'http://www.win4000.com/meinvtag4_1.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}


def parseXpath(html, xpath):
    return html.xpath(xpath).extract()


def parseXpathFirst(html, xpath):
    return html.xpath(xpath).extract_first()


def parseCss(html, css):
    return html.css(css).extract()


def getHtml(url):
    res1 = requests.get(url=url, headers=headers)
    result1 = res1.content.decode('utf-8')
    return parsel.Selector(result1)

def saveImgage(data_list, data_name_list):
    for i, url in enumerate(data_list):
    
        print(f'开始下载 {data_name_list[i]} ')
        
        img_file = './image/' + data_name_list[i]
        # if not os.path.exists(img_file):
        #     os.mkdir(img_file)
        
        # 获取图片 img_url_list
        html2 = getHtml(url)
        url_list = parseXpath(html2, '//div/ul[@id="scroll"]//a/img/@data-original')
        for i, img_url in enumerate(url_list):
            img_url = img_url.split('_')[0] + '.jpg'
            # 请求图片
            img_data = requests.get(url=img_url, headers=headers).content
           
            # 保存数据
            img_name = img_file + f'{i}.jpg'
            print(f'下载中 {img_name} ')
            
            with open(img_name, 'wb') as f:
                f.write(img_data)

def run():
    url = 'http://www.win4000.com/meinvtag4_1.html'
    
    for i in range(1, 5):
        url = f'http://www.win4000.com/meinvtag4_{i}.html'
        print(f'开始下载第 {i} 页数据, 共 5 页')
        html1 = getHtml(url)
        
        # 获取图片详情页url list
        data_list = parseXpath(html1, '//div[@class="Left_bar"]//li/a/@href')
        # 获取图片详情页 name
        data_name_list = parseXpath(html1, '//div[@class="Left_bar"]//li/a/p/text()')
        
        
        saveImgage(data_list, data_name_list)
        


if __name__ == '__main__':
    run()
    
    # if not os.path.exists('./image/' + ''):
    #     os.mkdir('')
