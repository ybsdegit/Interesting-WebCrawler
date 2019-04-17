#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 23:56
# @Author  : Paulson
# @File    : URLManager.py
# @Software: PyCharm
# @define  : function


class URLManager(object):
    """
    爬虫调度器，主要是配合调用其他四个模块，所谓调度就是取调用其他的模板
    在这里主要就是两个集合，一个是已爬取URL的集合，另一个是未爬取URL的集合。
    这里使用的是set类型，因为set自带去重的功能
    """
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        # 判断是否有未爬取过的url
        return self.new_url_size() != 0

    def get_new_url(self):
        # 获取一个未爬取的链接
        new_url = self.new_urls.pop()
        # 提取之后，将其添加到已经爬取过的链接中
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        # 将新链接添加到未爬取的集合中（单个链接）
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        # 将新链接添加到未爬取的集合中（集合）
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        # 获取未爬取url的大小
        return len(self.new_urls)

    def old_url_size(self):
        # 获取已爬取的url的大小
        return len(self.old_urls)
