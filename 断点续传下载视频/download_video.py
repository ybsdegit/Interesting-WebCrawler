#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/30 20:47
# @Author  : Paulson
# @File    : download_video.py
# @Software: PyCharm
# @define  : function
import os

import requests
from tqdm import tqdm


def down_from_url(url, dst):
    response = requests.get(url, stream=True) # (1)
    file_size = int(response.headers['content-length']) # (2)
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)  # (3)
    else:
        first_byte = 0
    if first_byte >= file_size: # (4)
        return True

    header = {"Range": f"bytes={first_byte}-{file_size}"}
    
    size = 0
    pbar = tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, stream=True)
    with open(dst, 'ab') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                size += len(chunk)
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size == size

url = "https://pic.ibaotu.com/00/51/34/88a888piCbRB.mp4"
print(down_from_url(url, "测试视频.mp4"))
