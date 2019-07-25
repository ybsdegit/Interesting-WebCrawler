#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/7/22 10:28
# @author: Paulson●Wier
# @file: spider.py
# @desc:
import requests
from lxml import etree

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
           'AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/74.0.3729.131 Safari/537.36',
           'Host': 'www.ctic.org'
           }

data = {
    '_csrf':'R3JmTC1uZy4DIikKHggvRxE0BwEAX1QaIBhUBWEZEWcBRQ81fh0gYA==',
    'CRMSearchForm[year]':'2011',
    'CRMSearchForm[format]':'Acres',
    'CRMSearchForm[area]':'County',
    'CRMSearchForm[region]':'Midwest',
    'CRMSearchForm[state]':'IL',
    'CRMSearchForm[county]':'Adams',
    'CRMSearchForm[crop_type]':'All',
    'summary':'county',
    }

def new_session():
    session = requests.Session()
    response = session.get(url, headers=headers)
    html = etree.HTML(response.text)
    return session, html

url = 'https://www.ctic.org/crm?tdsourcetag=s_pctim_aiomsg'

session, html = new_session()
csrf_token = html.xpath("//head/meta[@name=\"csrf-token\"]/@content")[0]
data.update({'_csrf': csrf_token})

response = session.post(url, data=data, headers=headers, timeout=30)
print(response.status_code)
if response.status_code == 200:
    with open('x.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

import pandas as pd

df = pd.read_html('x.html')[0]
print(df)