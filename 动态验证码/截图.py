#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:35
# @Author  : Paulson
# @File    : 截图.py
# @Software: PyCharm
# @define  : function
import time

from PIL import Image
from selenium import webdriver
# import tesserocr

# img = Image.open('image/cap_image.png')


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


def get_cap_number(img):
    image = image_grayscale_deal(img)
    image = image_thresholding_method(image)
    result = tesserocr.image_to_text(image)
    print(result)
    return result



def get_cap_image(driver):
    """
    截图获取验证码图片
    :param driver:
    :return: 验证码图片的二进制数据
    """
    driver.save_screenshot('login.png')
    image_element = driver.find_element_by_id('img_pic_code')
    location = image_element.location  # 获取验证码 x,y 坐标 左上角
    location['x'] += 20
    size = image_element.size  # 获取验证码的窗宽
    size['width'] -= 20
    rectangle = (location['x'], location['y'],
                 location['x'] + size['width'], location['y'] + size['height'])
    image = Image.open('login.png')
    frame = image.crop(rectangle)
    frame.save('cap_image.png')
    time.sleep(2)
    with open('cap_image.png', 'rb') as f:
        cap_image_content = f.read()
    return cap_image_content

    
def login(phone_number):
    login_url = 'https://www.95303.com/usercenter/login.html'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(login_url)
    driver.find_element_by_id('login_message_phone').send_keys(phone_number)  # 输入手机号
    
    cap_image_content = get_cap_image(driver)  # 验证码图片 -> byte二进制数据
    cap_image_number = get_cap_number(cap_image_content)
    
    driver.find_element_by_id('login_img_code').send_keys(cap_image_number)  # 输入图片验证码
    
    driver.find_element_by_xpath('//div[text()="点击发送短信验证码"]').click()  #
    cap_phone_number = 123456
    driver.find_element_by_id('login_message_password').send_keys(cap_phone_number) # 输入短信验证码
    driver.find_element_by_id('test_message_login').click()  # 登录
    
    
if __name__ == '__main__':
    phone_number = 18810911636
    login(phone_number)