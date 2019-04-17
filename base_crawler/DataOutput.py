#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 0:29
# @Author  : Paulson
# @File    : DataOutput.py
# @Software: PyCharm
# @define  : function
import codecs


class DataOutput(object):
    """
    数据存储器，就是将HTML下载器发送过来的数据存储到本地
    大家可能发现我这里是将数据存储到一个html的文件当中，在这里你当然也可以存在Mysql或者csv等文件当中，这个看自己的选择，我这里只是为了演示所以就放在了html当中。

    """

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open('baike.html', 'a', encoding='utf-8')
        fout.write("<html>")
        fout.write("<head><meta charset='utf-8'/></head>")
        fout.write("<body>")
        fout.write("<table>")
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            print(data['title'])
            fout.write("<td>《%s》</td>" % data['title'])
            fout.write("<td>[%s]</td>" % data['summary'])
            fout.write("</tr>")
            self.datas.remove(data)
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()
