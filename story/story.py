#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/14 23:59
# @Author  : Paulson
# @File    : story.py
# @Software: PyCharm
# @define  : function
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 21:25:45 2019
@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import random
import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr



def getHTMLText(url, headers):
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text

    except:
        return "爬取失败"


def parsehtml(namelist, urllist, html):
    url = 'http://www.tom61.com/'
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('dl', attrs={'class': 'txt_box'})
    # print(t)
    i = t.find_all('a')
    # print(i)
    for link in i:
        urllist.append(url + link.get('href'))
        namelist.append(link.get('title'))


def parsehtml2(html):
    text = []
    soup = BeautifulSoup(html, 'html.parser')
    t = soup.find('div', class_='t_news_txt')
    for i in t.findAll('p'):
        text.append(i.text)
    # print(text)
    return "\n".join(text)


def sendemail(url, headers):
    # msg = MIMEText("邮件正文", 'html', 'utf-8')
    # msg['From'] = u'<%s>' % from_addr
    # msg['To'] = u'<%s>' % to_addr
    # msg['Subject'] = subject
    #
    # smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
    # smtp.set_debuglevel(1)
    # smtp.ehlo("smtp.163.com")
    # smtp.login(from_addr, password)
    # smtp.sendmail(from_addr, [to_addr], msg.as_string())
    
    msg_from = '****@163.com'  # 发送方邮箱
    passwd = '*****'  # 填入发送方邮箱的授权码
    receivers = ['ybsdeyx@126.com,ybsdeyx@foxmail.com']  # 收件人邮箱
    
    subject = '今日份的睡前小故事'  # 主题
    html = getHTMLText(url, headers)
    print(html)
    content = parsehtml2(html)  # 正文
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = ','.join(receivers)
    s = smtplib.SMTP_SSL("smtp.163.com", 465)  # 邮件服务器及端口号
    try:
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg['To'].split(','), msg.as_string())
        print("发送成功")
    except:
        print("发送失败")
        raise
    finally:
        s.quit()


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        }

    urllist = []
    namelist = []
    for i in range(1, 3):
        if i == 1:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index.html'
        else:
            url = 'http://www.tom61.com/ertongwenxue/shuiqiangushi/index_' + str(i) + '.html'
        print("正在爬取第%s页的故事链接：" % (i))
        print(url + '\n')
        html = getHTMLText(url, headers)
        parsehtml(namelist, urllist, html)
    print("爬取链接完成")
    '''
    for i in urllist:
        html=getHTMLText(i,headers)
        parsehtml2(html)
    '''
    sendemail(random.choice(urllist), headers)


if __name__ == '__main__':
    main()
