#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 23:28
# @Author  : Paulson
# @File    : captcha.py
# @Software: PyCharm
# @define  : function

import requests


headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
}

login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
session = requests.Session()
session.get(login_url)

image_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand'
req = session.get(image_url, headers=headers).content
with open('code.png', 'wb') as f:
    f.write(req)
    
check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'




point_dict = {
    '1': '37,40',
    '2': '112,40',
    '3': '187,40',
    '4': '262,40',
    '5': '37,120',
    '6': '112,120',
    '7': '187,120',
    '8': '262,120',
}
def get_point(indexs):
    indexs = indexs.split(',')
    temp = []
    for index in indexs:
        temp.append(point_dict[index])
    return ','.join(temp)

params = {
'answer': get_point(input('请输入验证码位置')),
'rand':'sjrand',
'login_site':'E',
}
response = session.get(check_url, params=params, headers=headers).text
print(response)