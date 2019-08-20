#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/8/20 11:30
# @author: Paulson●Wier
# @file: common_wallhaven.py
# @desc:
import os
import bs4
import requests
import uuid
import time


url = 'https://alpha.wallhaven.cc/latest'
# https://wallhaven.cc/latest?page=4
dirName = r'.\image'  # 目录名称
os.makedirs(dirName, exist_ok=True)

img_url_list = []
def run(num=5):
    url_list = [f'https://wallhaven.cc/latest?page={i}' for i in range(1,num)]
    for singlePicUrl in url_list:
        res = requests.get(singlePicUrl)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        div = soup.find(id="thumbs")
        for i in div.find_all('li'):
            if i.find('img'):
                url = i.find('img')['data-src']
                url = url[url.find('small')+6:]
                x, y = url.split('/')
                url = 'https://w.wallhaven.cc/full/' + x + '/wallhaven-' + y
                img_url_list.append(url)


def save_img(img_download_url, path):

    image_id = str(uuid.uuid4())  # 当前网关和时间组成的随机字符串
    image_name = path+'\\'+image_id+'.jpg'
    response = requests.get(url=img_download_url)
    with open(image_name, 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    start = time.time()
    run(2)
    print(len(img_url_list))
    for url in img_url_list:
        save_img(url, dirName)
    end = time.time()
    cost = start - end
    print("时间:", cost)

