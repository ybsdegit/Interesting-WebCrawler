# python 爬取百度贴吧图片并保存——还有这种反爬策略！

> 昨天有人问我爬取百度贴吧图片使用xpath解析不了网页我说怎么回了，点了下网页，看着是比较简单啊，分分钟搞定。所以我就动手了。哎。人呐，就是不知道自己可以被预料，我一个好好地.....啥奇怪的东西。
> 接下来就动手了
> 人呐分割线 ----------------------------------------------------------------------------------------------------------------------------------
>发送请求，查看返回内容，么问题，0k！
> 解析数据 ，卧槽，xpath语句写的有问题吗？！！！
>各种尝试
```
'//div[@class="t_con cleafix"]/div/div/div/a/@href'
'//*[@id="thread_list"]/li/div/div[2]/div[1]/div[1]/a'
'//*[@id="thread_list"]]//div/div/a'
```
>总之就是不行
>难道本地lxml版本不对，更新，不管用
>换用BeautifulSoup试，也不可以
>到这个时候发现搞这个都1个小时了，烦躁的一批
>但不能慌啊，曾有人说过：一个人的命运啊，要靠个人的奋斗，更要看历史的进程啊
>一行代码一行的试了下
>到了这一行，UA，没毛病啊
```
self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}   
```
>Too Young  
>去掉UA最后边的 Chrome/74.0.3729.108 Safari/537.36
>邪魅一笑，成了。
```
self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '}   
```
> 接下来没啥好说的，5分钟撸完运行1分钟，随便看看结束。睡觉。

这里上代码
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/27 20:37
# @Author  : Paulson
# @File    : SpiderTieba.py
# @Software: PyCharm
# @define  : function
import os

import requests
from lxml import etree


class Spider(object):
    """
    爬取百度贴吧数据
    """
    def __init__(self):
        # self.query_string = query_string
        self.url = "https://tieba.baidu.com/f?"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '}   
        # 不能添加这一段，不然获取不到数据 Chrome/74.0.3729.108 Safari/537.36


    def params(self):
        para = {
            "kw": "女神"
        }
        return para

    def send_request(self, url, parms={}):
        """
        1. 发送请求
        :param url:
        :param param:
        :return:
        """
        response = requests.get(url, params=parms, headers=self.headers)
        # s = response.url
        # print(s)
        # with open('1.html', 'w', encoding='utf-8') as f:
        #     f.write(str(response.content.decode()))
        return response.content

    def parse_data(self, data, rule):
        """
        2. 数据解析
        :return:
        """
        html_data = etree.HTML(data)
        data_list = html_data.xpath(rule)
        return data_list

    def sava_data(self, data, image_name):
        """
        3. 保存数据
        :return:
        """
        os.makedirs('./images/', exist_ok=True)
        image_path = 'images/' + image_name
        with open(image_path, 'wb') as f:
            print('正在爬取: ', image_name)
            f.write(data)


    def run(self):
        """
        main逻辑
        :return:
        """
        tieba_params = self.params()
        datas = self.send_request(self.url, tieba_params)
        detail_rule = '//div[@class="t_con cleafix"]/div/div/div/a/@href'
        url_list = self.parse_data(datas, detail_rule)

        for lable in url_list:
            url = 'http://tieba.baidu.com' + lable
            detail_data = self.send_request(url)

            # 解析图片url
            image_url_rule = '//img[@class="BDE_Image"]/@src'
            image_url_list = self.parse_data(detail_data, image_url_rule)

            # 列表切片去图片名字
            for image_url_l in image_url_list:
                image_data = self.send_request(image_url_l)
                image_name = image_url_l[-12:]
                self.sava_data(image_data, image_name)


if __name__ == '__main__':
    # s_search = input("请输入查询关键字")
    tei_ba = Spider()
    tei_ba.run()

```

# 
## 果然学好姿势很重要，努力
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190430002518424.gif)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190430002349231.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM4NTM0MTA3,size_16,color_FFFFFF,t_70)
