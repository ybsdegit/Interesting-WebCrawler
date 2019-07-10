#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 23:39
# @Author  : Paulson
# @File    : headers.py
# @Software: PyCharm
# @define  : function

import re

headers_str ="""
Accept: image/webp,image/apng,image/*,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7
Connection: keep-alive
Cookie: gr_user_id=f9c2eb7b-eb0b-4724-9cc0-3a0b1bdee0d9; 8191c76fea6b7aaa_gr_session_id=11c9ce3b-f3a0-47a7-a700-1985c1af93ad; 8191c76fea6b7aaa_gr_session_id_11c9ce3b-f3a0-47a7-a700-1985c1af93ad=true; grwng_uid=816387bc-e279-4489-b064-e85d649aa2e4; www.95303.com=1562766283515; PHPSESSID=eja4o9gkbh1p7f27rhnla2fcg3
Host: www.95303.com
Referer: https://www.95303.com/usercenter/login.html
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36
"""
pattern = '^(.*?): (.*)$'

for line in headers_str.splitlines():
    print(re.sub(pattern,'\'\\1\':\'\\2\',', line))