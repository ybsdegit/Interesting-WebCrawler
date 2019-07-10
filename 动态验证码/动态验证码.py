#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 21:47
# @Author  : Paulson
# @File    : 动态验证码.py
# @Software: PyCharm
# @define  : function
from requests import session
import requests
from selenium import webdriver



url_login = 'https://www.95303.com/usercenter/login.html'
url_cap = 'https://www.95303.com/api/User/Send_tel_identifying?&type=2&phoneid=93354036'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url_login)
cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
cookiestr = ';'.join(item for item in cookie)
headers = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection':'keep-alive',
    'Cookie':cookiestr,
    # 'Cookie':'gr_user_id=f9c2eb7b-eb0b-4724-9cc0-3a0b1bdee0d9; 8191c76fea6b7aaa_gr_session_id=11c9ce3b-f3a0-47a7-a700-1985c1af93ad; 8191c76fea6b7aaa_gr_session_id_11c9ce3b-f3a0-47a7-a700-1985c1af93ad=true; grwng_uid=816387bc-e279-4489-b064-e85d649aa2e4; www.95303.com=1562766283515; PHPSESSID=eja4o9gkbh1p7f27rhnla2fcg3',
    'Host':'www.95303.com',
    'Referer':'https://www.95303.com/usercenter/login.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

# session.cookies = cookies
url_image = driver.find_element_by_id('img_pic_code').get_attribute('src')
print(url_image)
session = session()
res = session.get(url_image, headers=headers).content
# response = session.get()
# res = session.get(url_login, headers=headers)
# print(res.status_code)
# res = session.get(url_cap, headers=headers).content
with open('cap.png', 'wb') as f:
    f.write(res)



