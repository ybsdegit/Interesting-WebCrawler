#!/usr/bin/env python
# encoding: utf-8
# @software: PyCharm
# @time: 2019/8/5 9:57
# @author: Paulson●Wier
# @file: use_tesserocr.py
# @desc:
import time
import tesserocr
from PIL import Image

image = Image.open('code.png')

image = image.convert('L')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
result = tesserocr.image_to_text(image)
print(result)