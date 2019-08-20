#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/8/20 14:12
# @author: Paulson●Wier
# @file: asynicio_wallhaven.py
# @desc:
import traceback

from aiohttp_requests import requests
import asyncio
import aiofiles
import os
import bs4
import uuid
import time

dirName = r'.\image'  # 目录名称
os.makedirs(dirName, exist_ok=True)

async def get_image_url_list(num=5):
    url_list = [f'https://wallhaven.cc/latest?page={i}' for i in range(1,num)]
    img_list = []
    for singlePicUrl in url_list:
        res = await requests.get(singlePicUrl)
        soup = bs4.BeautifulSoup(await res.text(), "lxml")
        div = soup.find(id="thumbs")
        for i in div.find_all('li'):
            if i.find('img'):
                url = i.find('img')['data-src']
                url = url[url.find('small')+6:]
                x, y = url.split('/')
                url = 'https://w.wallhaven.cc/full/' + x + '/wallhaven-' + y
                img_list.append(url)
    return img_list


async def save_img(img_download_url, num_img, path):
    try:
        print(f'开始下载图片：{num_img}', img_download_url)
        image_id = str(uuid.uuid4())  # 当前网关和时间组成的随机字符串
        image_name = path + '\\' + image_id + f'{num_img}.jpg'
        response = await requests.get(url=img_download_url)
        async with aiofiles.open(image_name, 'wb') as f:
            await f.write(await response.read())
            print(f'{image_name} 保存完成')

    except:
        traceback.print_exc()
        print("下载失败：", img_download_url)


async def run(num):
    start = time.time()

    img_list = await get_image_url_list(num)
    print(len(img_list))

    num_img = 0
    tasks = []
    for img_url in img_list:
        num_img += 1
        tasks.append(save_img(img_url, num_img, dirName))
    await asyncio.gather(*tasks)

    end = time.time()
    cost = end - start
    print("爬取结束，时间:", cost)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(num=2))