#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/7 22:42
# @Author  : Paulson
# @File    : crawler.py
# @Software: PyCharm
# @define  : function
# 千千静听榜单音乐下载

from parsel import Selector
import requests
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
}
base_url = 'http://music.taihe.com'
music_info_base_url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&songid='


def getHtml(url):
    return Selector(requests.get(url=url, headers=headers).content.decode())

def getStr(url):
    return requests.get(url).content.decode()


def parseXpath(html, xpath):
    return html.xpath(xpath).extract()


def run():
    res = getHtml(base_url + '/top/')
    billboard_names = parseXpath(res, '//dd/a/text()')
    billboard_hrefs = parseXpath(res, '//dd/a/@href')
    
    for billboard_name, billboard_href in zip(billboard_names, billboard_hrefs):
        billboard_url = base_url + billboard_href
        music_directory = f'./{billboard_name}'
        print(music_directory)
        if not os.path.exists(music_directory):
            os.mkdir(music_directory)

        html = getHtml(billboard_url)
        music_urls = parseXpath(html, '//span[@class="song-title "]/a[1]/@href')
        music_names = parseXpath(html, '//span[@class="song-title "]/a[1]/text()')

        for music_url, music_name in zip(music_urls, music_names):
            music_info_url = music_info_base_url + music_url.split('/')[-1]
            music_down_url = json.loads(getStr(music_info_url))['bitrate']['show_link']
            music_name = f'{music_directory}/{music_name.replace("/", "")}.mp3'
            print(f'===正在下载:{music_name.replace("./", "")}===')
            with open(music_name, 'wb') as f:
                f.write(requests.get(music_down_url).content)


if __name__ == '__main__':
    print("====开始下载====")
    run()
    print("====下载结束====")
