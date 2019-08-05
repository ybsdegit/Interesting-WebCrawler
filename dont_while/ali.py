#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/4 21:33
# @Author  : Paulson
# @File    : ali.py
# @Software: PyCharm
# @define  : function

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput.keyboard import Key, Controller as c2
from pynput.mouse import Button, Controller as c1


class vcg_get_cookies():
    mouse = c1()
    url = 'https://www.vcg.com/login'
    options = webdriver.ChromeOptions()
    # 不加载图片,加快访问速度
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 添加本地代理
    # options.add_argument("--proxy--server=127.0.0.1:8080")
    # 添加UA
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    options.add_argument('user-agent=' + ua)
    
    # driver = webdriver.Chrome(executable_path="D:\chromedriver.exe", options=options)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    time.sleep(3)
    driver.refresh()
    while True:
        # pyautogui.press('f5')
        # keyboard.press(Key.f5)
        driver.refresh()
        time.sleep(3)
        mouse.position = (1562, 400)
        mouse.press(Button.left)
        time.sleep(1)
        mouse.move(1890, 498)
        time.sleep(1)
        mouse.release(Button.left)
        time.sleep(3)
        WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, 'nc-lang-cnt')))
        if driver.find_element_by_class_name('nc-lang-cnt').text == '验证通过':
            break
    
    time.sleep(2)
    driver.find_element_by_name('id').send_keys('用户名')
    time.sleep(2)
    driver.find_element_by_name('password').send_keys('123456')
    driver.find_element_by_class_name('sign-in-form__btn').click()
    time.sleep(5)
    user_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'userInfo')))
    print(user_name)
    cookies = driver.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
    driver.close()  # 获取cookies便可以关闭浏览器
    # 然后的关键就是保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的
    # 当然可以把cookies返回回去，但是之后的每次请求都要先执行一次login没有发挥cookies的作用
    jsonCookies = json.dumps(cookies)  # 通过json将cookies写入文件
    with open('vcgCookies.json', 'w') as f:
        f.write(jsonCookies)
    print(cookies)