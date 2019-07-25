#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 21:46
# @Author  : Paulson
# @File    : 糗事百科.py
# @Software: PyCharm
# @define  : function
import json

import requests
from lxml import etree


class Spider():
    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
        
    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(1, 14)]
    
    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()
    
    def get_content_list(self, html_str):
        """提取数据"""
        html = etree.HTML(html_str)
        div_list = html.xpath('//*[@id="content-left"]/div')  # 分组
        content_list = []
        for div in div_list:
            item = {}
            item['content'] = div.xpath('.//div[@class="content"]/span/text()')
            item['content'] = [i.replace("\n", "") for i in item['content']]
            item['articleGender'] = div.xpath('.//div[contains(@class, "articleGender")]/@class')
            item['articleGender'] = item['articleGender'][0].split(" ")[-1].replace('Icon', '') if len(item['articleGender']) > 0 else None
            item['author_age'] = div.xpath('.//div[contains(@class, "articleGender")]/text()')
            item['author_age'] = item['author_age'][0] if len(item['author_age']) > 0 else None
            item['content_img'] = div.xpath('.//div[class="thumb"]/a/img/@src')
            item['content_img'] = "https:" + item['content_img'][0] if len( item['content_img'] ) > 0 else None
            item['author_img'] = div.xpath('.//div[@class="author clearfix"]//img/@src')
            item['author_img'] = "https:" + item['author_img'][0] if len(item['author_img']) > 0 else None
            item['stats_vote'] = div.xpath('.//span[@class="stats-vote"]/i/text()')
            item['stats_vote'] = item['stats_vote'][0] if len(item['stats_vote']) > 0 else None
            item['stats-comments'] = div.xpath('.//span[@class="stats-comments"]/a/i/text()')
            item['stats-comments'] = item['stats-comments'][0] if len( item['stats-comments']) > 0 else None
            content_list.append(item)
        return content_list
    
    def save_content_list(self, content_list):
        for i in content_list:
            with open('糗事百科.txt', 'a+', encoding='utf-8') as f:
                f.write(json.dumps(i, ensure_ascii=False))
                f.write('\n')
    
    def run(self):
        # 1. url_list
        url_list = self.get_url_list()
        
        # 2. 遍历，发送请求， 获取响应
        for url in url_list:
            html_str = self.parse_url(url)
        # 3. 提取数据
            print('开始爬取：',url)
            content_list = self.get_content_list(html_str)
            print(content_list)
            
        # 4. 保存数据
            self.save_content_list(content_list)
        
        
if __name__ == '__main__':
    spider = Spider()
    spider.run()
