#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 20:46
# @Author  : Paulson
# @File    : key_mouse.py
# @Software: PyCharm
# @define  : function

import time
from pynput.keyboard import Controller as key_cl
from pynput.mouse import Button, Controller
from pynput import mouse
import keyword

def keyword_input(string):
    keyboard = key_cl()
    keyboard.type(string)


def mouse_click():
    mouse = Controller()
    mouse.press(Button.left)
    mouse.release(Button.left)
    

def main(number, string):
    time.sleep(7)
    for i in range(number):
        keyword_input(f'{string}')
        mouse_click()
        time.sleep(0.1)
        

if __name__ == '__main__':
    main(10, "马媛媛是最漂亮的！")