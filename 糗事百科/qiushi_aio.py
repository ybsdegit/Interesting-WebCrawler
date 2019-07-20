#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/20 14:20
# @Author  : Paulson
# @File    : qiushi_aio.py
# @Software: PyCharm
# @define  : function

import asyncio
import aiohttp

from lxml import html

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}

async def getsourse(url):
    conn = aiohttp.TCPConnector(verify_ssl=False)  # 防止ssl报错
    async with aiohttp.ClientSession(connector=conn) as session:  # 创建session
        async with session.get(url, headers=headers, timeout=20) as req:  # 获得请求
            if req.status == 200:  # 判断请求码
                sourse = await req.text()  # 使用await关键字获取返回结果
            else:
                print("访问失败")


if __name__ == '__main__':
    full_urllist = ["https://www.baidu.com", "https://www.cnblogs.com", "https://www.jianshu.com"]
    event_loop = asyncio.get_event_loop()  # 创建事件循环
    tasks = [getsourse(url) for url in full_urllist]
    results = event_loop.run_until_complete(asyncio.wait(tasks))
