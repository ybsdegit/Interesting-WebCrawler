#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/4 20:31
# @Author  : Paulson
# @File    : white.py
# @Software: PyCharm
# @define  : function

import pyautogui
import time

pyautogui.FAILSAFE = True

# time.sleep(3)
while True:
    region=(644, 520, 320, 20)
    im = pyautogui.screenshot(region=region)
    im.save('test.png')

    # x = 40, y = 10
    for i in range(40, 300, 80):
        px = im.getpixel((i+20, 5))
        print(px)
        if px[0] == 2:
            pyautogui.click(region[0] + i, region[1] + 10)
            # time.sleep(0.05)


