#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 0:11
# @Author  : Paulson
# @File    : HTMLDownload.py
# @Software: PyCharm
# @define  : function
import requests


class HTMLDownload(object):
    """
    HTML下载器，就是将要爬取的页面的HTML下载下来
    """
    def download(self, url):
        if url is None:
            return
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) ' \
                                  'Chrome / 63.0.3239.132Safari / 537.36'
        res = s.get(url)

        # 判断是否正常获取
        if res.status_code == 200:
            # print(res.text)
            res.encoding = 'utf-8'
            res = res.text
            # res.encode('utf-8')
            return res
        return None


