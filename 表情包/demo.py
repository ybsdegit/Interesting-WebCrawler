#!/usr/bin/python3
# encoding: utf-8
# time : 2019/6/1 20:31
import asyncio
from itertools import islice
from typing import Generator
import aiofiles as aiofiles
import aiohttp
import async_timeout
import uuid
import pathlib
from lxml import html

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass
import traceback

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

sem = asyncio.Semaphore(500)

dir_path = pathlib.Path.cwd()


def iter_list():
    """
    Domain_list.txt 里面有不同的url地址，100W行左右
     可以用这个测试
    :return:
    """
    # all_url = []
    f_path = dir_path / "top-1m.csv"
    with open(f_path) as input_file:
        gen_urls = [f"http://wwww.{i.strip().split(',')[-1]}" for i in input_file.readlines() if i]
        return gen_urls


async def save_txt(source):
    """

    :param source:
    :return:
    """
    try:
        f_path = dir_path / "baidu"
        html_path = str(f_path / f"{uuid.uuid1()}.html")
        async with aiofiles.open(html_path, 'wb') as f:
            await f.write(source)
    except Exception as e:
        print(e.args)


async def parse(url, source: str):
    root = html.fromstring(source)
    title = root.xpath("//head//title//text()")
    print(url, title)


async def fetch(item, session):
    """
    用的百度测试的
    :param item:
    :param session:
    :return:
    """
    try:
        # async with session.post(url=item, headers=headers, timeout=20) as req:
        with async_timeout.timeout(5):
            async with session.get(url=item, headers=headers) as req:
                source = await req.text()
                if req.status in [200, 201]:
                    await parse(item, source)

                else:
                    await print(f'{item},{req.status()}')


    except Exception as e:
        print(item, e.args)


async def bound_fetch(url, session):
    # Getter function with semaphore.

    async with sem:
        await fetch(url, session)


async def run(gen_urls: Generator):
    tasks = []
    tc = aiohttp.TCPConnector(limit=100, enable_cleanup_closed=True, force_close=True, verify_ssl=False)
    async with aiohttp.ClientSession(connector=tc) as session:
        stop = False
        while not stop:
            try:
                index = 0
                for i in islice(gen_urls, index, index + 1000):
                    if not i:
                        stop = True
                        break
                    task = asyncio.ensure_future(bound_fetch(i, session))
                    tasks.append(task)
                asyncio.wait(tasks)
                index += 1000
                await asyncio.sleep(0.1)
            except Exception as e:
                print(e.args)
                break


if __name__ == '__main__':
    gen_urls = iter_list()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(gen_urls))
    loop.run_until_complete(future)
