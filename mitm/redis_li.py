#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/9 0:41
# @Author  : Paulson
# @File    : redis_li.py
# @Software: PyCharm
# @define  : function

import redis
conn = redis.StrictRedis(host='192.168.182.128', port=6379, db=0)
conn.set('k1','v2') # 向远程redis中写入了一个键值对
val = conn.get('k1') # 获取键值对
print(val)