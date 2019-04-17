#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/17 21:51
# @Author  : Paulson
# @File    : bilibuli.py
# @Software: PyCharm
# @define  : function
import datetime
import json
import time
import pandas as pd
import requests
from B站鬼畜.config import START, END

url = 'https://s.search.bilibili.com/cate/search?callback=' \
      'jqueryCallback_bili_5930824530966949&main_ver=v3&search_type=' \
      'video&view_type=hot_rank&order=click&copy_right=-1&cate_id=22&page=1&' \
      'pagesize=20&jsonp=jsonp&time_from=20190410&time_to=20190417&_=1555509605545'



def get_list(j, start, end):

        try:
            url = 'https://s.search.bilibili.com/cate/search?callback=jqueryCallback_bili_06768280565043483' \
                  '&search_type=video&view_type=hot_rank&order=click&cate_id=22&page={}' \
                  '&pagesize=20&time_from={}&time_to={}'.format(str(j),str(start),str(end))
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
                  'Connection': 'keep-alive'}
            cookies = 'v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
            cookie = {}
            for line in cookies.split(';'):
                name, value = cookies.strip().split('=', 1)
                cookie[name] = value
            html = requests.get(url, cookies = cookie, headers = header).content
            # print(html.json())
            print(json.loads(html.decode('utf-8')))
            info = json.loads(html.decode('utf-8'))['result']
            print(info)
            return info
        except:
           pass

guichu_all = []
for i in range(1):
    this_guichu = get_list(i, START, END)
    guichu_all = guichu_all + this_guichu
    # print('')

guichu = pd.DataFrame()
guichu['title'] = [k['title'] for k in guichu_all]
guichu['arcurl'] = [k['arcurl'] for k in guichu_all]
guichu['pic'] = [k['pic'] for k in guichu_all]
guichu['author'] = [k['author'] for k in guichu_all]
guichu['period'] = [k['duration'] for k in guichu_all]
guichu['play'] = [int(k['play']) if k['play'] != '--' else 0 for k in guichu_all]
guichu['danmu'] = [k['video_review'] for k in guichu_all]
guichu['arcurl'] = [k['arcurl'] for k in guichu_all]
guichu['favorites'] = [k['favorites'] for k in guichu_all]
guichu['review'] =  [k['review'] for k in guichu_all]
guichu['tag'] =  [k['tag'].split(',') for k in guichu_all]
guichu['date'] =  [k['pubdate'][0:10] for k in guichu_all]
guichu['month'] = [k['pubdate'][0:7] for k in guichu_all]
guichu['year'] = [k['pubdate'][0:4] for k in guichu_all]
guichu['time'] =  [k['pubdate'][11:19] for k in guichu_all]

week_num = [datetime.date(int(k['pubdate'][0:4]),int(k['pubdate'][5:7]),
                  int(k['pubdate'][8:10])).isocalendar() for k in guichu_all]
guichu['week'] = [str(k[0])+'-0'+ str(k[1]) if k[1]<10 else str(k[0])+'-'+ str(k[1]) for k in week_num]
print(guichu)


