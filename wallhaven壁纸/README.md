【2019.08.20 python 下载壁纸原图 wallhaven， 使用同步异步方式进行对比 aiohttp_requests，aiofiles】

`本次主要是研究分别使用同步异步的方式下载壁纸原图`
'https://alpha.wallhaven.cc/latest'在速度方面的差异

## 使用模块
- 同步
使用 requests bs4

- 异步
使用 aiohttp_requests aiofiles asyncio


> 使用同步的方式，下载24张壁纸原图，花费时间为：

由于下载壁纸原图，太慢了，等不了
```cython
#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/8/20 11:30
# @author: Paulson●Wier
# @file: 异步_wallhaven.py
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


```


> 使用异步的方式

> aiohttp aiofiles

> 下载24张壁纸原图，花费时间为：

可以说异步的方式下载壁纸原图也没有很快, 共70M,用时249.2482135295868 也花费的4分钟多
可能是公司的网络真的是不友好，回家了可以再试试


```python
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
    cost = start - end
    print("爬取结束，时间:", cost)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(num=2))
```
