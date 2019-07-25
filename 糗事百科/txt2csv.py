#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 23:21
# @Author  : Paulson
# @File    : txt2csv.py
# @Software: PyCharm
# @define  : function

def txt2csv(txt_filename, csv_filename):
    txt_content_list = []
    csv_content = ''
    with open(txt_filename, 'r', encoding='utf-8') as f:
        txt_content = f.read()
    for i in txt_content:
        txt_content_list.append(i)
    
    csv_content = ','.join(txt_content_list)
    with open(csv_filename, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
if __name__ == '__main__':
    txt2csv('1.txt', '1.csv')