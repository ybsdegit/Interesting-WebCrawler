#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 0:10
# @Author  : Paulson
# @File    : biaoqingbao.py
# @Software: PyCharm
# @define  : function
import os
from time import time

import requests
from bs4 import BeautifulSoup
from queue import Queue
# from threading import Thread
import threading

class Spider(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        while True:
            url = self.queue.get()
            try:
                download_biaoqingbao(url)
            finally:
                self.queue.task_done()
    
def download_biaoqingbao(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')
   
    for img in img_list:
        image = img.get('data-original')
        title = img.get('title')
        print('下载图片： ', title)
    
        try:
            with open('./image/' + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print('length  failed')
            break


if __name__ == '__main__':
    start = time()
    
    _url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [_url.format(page=page) for page in range(1, 4000)]
    print(urls[:10])
    
    queue = Queue()
    
    # 创建线程
    for x in range(10):
        worker = Spider(queue)
        worker.daemon = True
        worker.start()
    
    # 加入队列
    for i in urls:
        queue.put(i)
        
    queue.join()
    print('下载完毕： 耗时', time() - start)
    