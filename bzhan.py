#encoding:utf-8
#author:simple
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from PIL import Image
from selenium.webdriver import ActionChains
import random


def get_snap(driver):
    driver.save_screenshot('snap.png')
    snap_obj = Image.open('snap.png')
    return snap_obj


def get_image(driver):
    image = driver.find_element_by_class_name('geetest_canvas_slice')
    time.sleep(1)
    size = image.size
    location = image.location
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']
    snap_obj = get_snap(driver)
    img_obj = snap_obj.crop((left, top, right, bottom))
    img_obj.save('image1.png')
    for i in range(1, 11):
        image2 = Image.open('image{}.png'.format(str(i)))
        rgb = (image2.load()[58, 20])
        rgb2 = (img_obj.load()[58, 20])
        if rgb[0] == rgb2[0] and rgb[1] == rgb2[1] and rgb[2] == rgb2[2]:
            img_obj.save('image1.png')
            return img_obj, image2


def find_jl(image_obj1, image_obj2):
    start_x = 58
    # 从坐标系（58,10开始往下扫描)
    start_y = 10
    for x in range(start_x, image_obj1.size[0]):
        for y in range(start_y, image_obj1.size[1] - 16):
            rgb = image_obj1.load()[x, y]
            rgb2 = image_obj2.load()[x, y]
            if abs(rgb[0] - rgb2[0]) > 60 and abs(rgb[1] - rgb2[1]) > 60 and abs(rgb[2] - rgb2[2]) > 60:
                # print(rgb)
                return x - 6


def get_tracks(distance):
    distance += 20
    # v = V0+a*t
    # S = v*t+0.5*a*(t**2)
    v0 = 0
    s = 0
    t = 0.4
    mid = distance * 3 / 5
    forward_tracks = []
    back_tracks = [-1, -1, -1, -1, -2, -2, -2, -2, -3, -3, -3, 1]
    while s < distance:
        if s < mid:
            a = 2
        else:
            a = -3
        v = v0
        track = v * t + 0.5 * a * (t ** 2)
        track = round(track)
        v0 = v + a * t
        s += track
        forward_tracks.append(track)
    return forward_tracks, back_tracks


def RUN(driver, track):
    slider_button = driver.find_element_by_class_name('geetest_slider_button')
    ActionChains(driver).click_and_hold(slider_button).perform()
    time.sleep(0.3)
    for i in track[0]:
        ActionChains(driver).move_by_offset(xoffset=i, yoffset=0).perform()
    time.sleep(0.2)
    for j in track[1]:
        ActionChains(driver).move_by_offset(xoffset=j, yoffset=0).perform()
    time.sleep(0.3)
    random_number = random.uniform(0, 2)
    ActionChains(driver).move_by_offset(xoffset=-random_number, yoffset=0).perform()
    time.sleep(random.uniform(0.5, 1))
    ActionChains(driver).move_by_offset(xoffset=random_number, yoffset=0).perform()
    ActionChains(driver).release().perform()


def main(user_id, password):
    # os.system("taskkill /f /im chromedriver.exe")
    url = 'https://passport.bilibili.com/login'
    # 1.登录页面
    driver = webdriver.Chrome()
    timeout = WebDriverWait(driver, 3)
    driver.get(url)
    # 2.输入账号和密码点登录
    timeout.until(EC.element_to_be_clickable((By.ID, 'login-username')))
    user_button = driver.find_element_by_id('login-username')
    user_button.send_keys(user_id)
    time.sleep(random.uniform(0, 1))
    password_button = driver.find_element_by_id('login-passwd')
    password_button.send_keys(password)
    login_button = driver.find_element_by_class_name('btn-login')
    login_button.click()
    time.sleep(1)
    # 3.得到滑动图片
    # for i in range(100):
    #     if i >= 1:
    #         driver.find_element_by_class_name('geetest_panel_error_content').click()
    #         time.sleep(1)
    #     for j in range(5):
    #         # get_image(driver, str(i)+str(j))
    #         time.sleep(0.5)
    #         driver.find_element_by_class_name('geetest_refresh_1').click()
    #         time.sleep(1)
    image_obj = get_image(driver)
    print(image_obj[0],image_obj[1])
    # 4.计算滑动距离
    distance = find_jl(image_obj[0], image_obj[1])
    print(distance)
    # 5.通过匀加速位移度算法,算出人手滑动轨迹
    track = get_tracks(distance)
    # 6.执行
    RUN(driver, track)
    # 7.关闭浏览器
    time.sleep(5)
    driver.close()


if __name__ == '__main__':
    user_id = ''
    password = ''
    main(user_id, password)