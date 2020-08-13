#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 22:51
# @Author  : Paulson
# @File    : everyday_english.py
# @Software: PyCharm
# @define  : function

from parsel import Selector
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class everyday_english():
    def __init__(self):
        self.url_list = "https://www.36yi.cn/c/sentence"
        self.url_detail = "https://www.36yi.cn/sentence/{}.html"
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        }
        
    def get_content(self):
        content = requests.get(self.url_list, self.headers).content.decode()
        content = Selector(content)
        article_id = content.xpath('//div[@class="entries"]/article[1]/@id').extract_first()
        article_id = article_id.split('-')[-1]
        
        content = requests.get(self.url_detail.format(article_id), self.headers).content.decode()
        content = Selector(content)
        title = content.xpath('//*[@class="page-title"]').extract_first()
        body = content.xpath('//*[@class="entry-content"]/p').extract()
        article_content = title + str("".join(body))
        print(content.xpath('//*[@class="page-title"]/text()').extract_first())
        return article_content
    
    def send_mail(self):
        body = self.get_content()
        msg = MIMEMultipart()
        msg_from = 'ybsdeyx@163.com'  # 发送方邮箱
        passwd = ''  # 填入发送方邮箱的授权码
        receivers = ['ybsdeyx@126.com,ybsdeyx@foxmail.com']  # 收件人邮箱
    
        subject = '今日份的想念'  # 主题
        mail_body  = MIMEText(body, _subtype='html', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = ','.join(receivers)
        msg.attach(mail_body )
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
        
    def run(self):
        self.send_mail()
        

if __name__ == '__main__':
    s = everyday_english()
    s.send_mail()