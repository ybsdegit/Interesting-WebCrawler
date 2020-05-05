#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/10 16:21
# @Author  : Paulson
# @File    : biaoqing.py
# @Software: PyCharm
# @define  : function
import requests
from lxml import etree
import os
from threading import Thread
from queue import Queue
from time import time


class DownloadBiaoqingbao(Thread):
    def __init__(self, queue, path):
        Thread.__init__(self)
        self.queue = queue
        self.path = './baoqingbao/'
        if not os.path.exists(path):
            os.mkdir(path)
            
    def run(self) -> None:
        while True:
            url = self.queue.get()
            try:
                download_biaoqingbaos(url, self.path)
            finally:
                self.queue.task_done()


def download_biaoqingbaos(url, path):
    response = requests.get(url)
    html = etree.HTML(response.content)
    img_list = html.xpath('//div//img[@class="ui image lazy"]')
    for img in img_list:
        image = img.get('data-original')
        title = img.get('title')
        # print(image, title)
        print('下载图片: ', title)

        try:
            with open(path + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except:
            pass


if __name__ == '__main__':
    
    start = time()
    
    # 构建所有的链接
    _url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [_url.format(page=page) for page in range(1, 200 + 1)]

    queue = Queue()
    path = './baoqingbao/'
    
    # 10个线程
    for x in range(10):
        worker = DownloadBiaoqingbao(queue, path)
        worker.daemon = True
        worker.start()
        
    for url in urls:
        queue.put(url)
    
    queue.join()

    print('下载完毕耗时：  ', time() - start)