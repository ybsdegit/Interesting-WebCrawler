#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 22:06
# @Author  : Paulson
# @File    : 异步_糗事.py
# @Software: PyCharm
# @define  : function


import asyncio
import time
import aiohttp
import requests
from lxml import etree
import pyttsx3


# table表格用于储存书本信息
list_urls = []
detail_urls = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Cookie': '_xsrf=2|531e2dce|3b7323fb97f9539aa647fc7dd83e18b4|1563540730; _qqq_uuid_="2|1:0|10:1563540731|10:_qqq_uuid_|56:ZmQ2ZDU5Njc2ODkyNWZkYTk1MzFiYWU2ZmI2YjMyNjk1ZmE4NDU3Nw==|b757bda41692c0d7b4ec25af3e8aadec2a2cc8aecab2b397a3d15bd2e41596dc"; _ga=GA1.2.1152470899.1563540730; _gid=GA1.2.2060768404.1563540730; __cur_art_index=7403; _gat=1',
    'Host': 'www.qiushibaike.com'
}


def parse_url(url):
    """解析列表页"""
    try:
        return requests.get(url, headers=headers, timeout=10).text
    except TimeoutError as msg:
        print('爬取异常'+str(msg))


async def fetch(url):
    """获取详情页"""
    try:
        conn = aiohttp.TCPConnector(verify_ssl=False)  # 防止ssl报错
        async with aiohttp.ClientSession(connector=conn) as session:  # 创建session
            # 创建session
            async with session.get(url, headers=headers, timeout=20) as req:  # 获得请求
                if req.status == 200:  # 判断请求码
                    # print(await req.text())
                    response = await req.text() # 使用await关键字获取返回结果
                    return response
                else:
                    print("访问失败")
    except:
        pass

def get_parse_info(response, patten):
    """解析网页"""
    html = etree.HTML(response)
    info = html.xpath(patten)
    return info


async def get_parse_detail(response, patten):
    """解析网页"""
    # print(response)
    html = etree.HTML(response)
    info = html.xpath(patten)
    return info


async def save_file(file_name, content):
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(','.join(content))
        f.write('\n')


async def parse_info(detail_content):
    detail_content = await get_parse_detail(detail_content, patten='//div[@class="content"]/text()')
    return detail_content

async def get_last_info(detail_url):
    
    detail_content = await fetch(detail_url)
    if detail_content != None:
        detail_info_list = await parse_info(detail_content)
        print(detail_info_list)
        await save_file('aio.txt',detail_info_list)
        
async def run(url):
    response = await fetch(url)
    # response = parse_url(url)
    list_info = []
    list_info = await get_parse_detail(response, patten='//a[@class="contentHerf"]/@href')
    # list_info.extend(list_info)
    
    
    list_urls_info = ['https://www.qiushibaike.com' + str(info) for info in list_info]
    print(len(list_urls_info))
   
    
    for detail_url in list_urls_info:
        detail_content = await fetch(detail_url)
        if detail_content != None:
            detail_info_list = await parse_info(detail_content)
            print(detail_info_list)
            await save_file('aio.txt', detail_info_list)

if __name__ == '__main__':
    start = time.time()
    num = 2
    urls =  [f'https://www.qiushibaike.com/text/page/{url}' for url in range(1, 51)]
   

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(run(url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)
    end = time.time()
    print('总共耗时{}秒'.format(end-start))
    

