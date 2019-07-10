#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 0:13
# @Author  : Paulson
# @File    : tesserocr_test.py
# @Software: PyCharm
# @define  : function

import tesserocr
from PIL import Image
import cv2

img = Image.open('image/cap_image.png')


def image_grayscale_deal(image):
    """
    图片转灰度处理
    :param image:图片文件
    :return: 转灰度处理后的图片文件
    """
    image = image.convert('L')
    # 取消注释后可以看到处理后的图片效果
    # image.show()
    return image


def image_thresholding_method(image):
    """
    图片二值化处理
    :param image:转灰度处理后的图片文件
    :return: 二值化处理后的图片文件
    """
    # 阈值，控制二值化程度，自行调整（不能超过256）
    threshold = 180
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # 图片二值化，此处第二个参数为数字一
    image = image.point(table, '1')
    # 取消注释后可以看到处理后的图片效果
    image.show()
    return image

image = image_grayscale_deal(img)
image = image_thresholding_method(image)
result = tesserocr.image_to_text(image)
print(result)
