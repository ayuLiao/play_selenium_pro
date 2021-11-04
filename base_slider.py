import os
import time
import base64
import random

from selenium import webdriver

from utils.pid import get_pid_track
from configs import root_path


class BaseSlider:
    @staticmethod
    def save_base64_img(browser, css, img_name):
        """
        save canvas use javascript
        :param browser:
        :param css: canvas css path
        :param img_name: canvas image save name
        """

        time.sleep(2)
        js = f'''
        return document.querySelector("{css}").toDataURL("image/png")
        '''
        base64_data = browser.execute_script(js)
        base64_data = base64_data.split(',')[1]
        img_bytes = base64.b64decode(base64_data)
        img_path = os.path.join(root_path, 'imgs', img_name)
        with open(img_path, 'wb') as f:
            f.write(img_bytes)
        return img_path

    @staticmethod
    def move_slider_track(browser, slider, track):
        ac = webdriver.ActionChains(driver=browser, duration=10)
        ac.click_and_hold(slider).perform()
        for x in track:
            offset_y = random.uniform(-2, 2)
            ac.move_by_offset(xoffset=x, yoffset=offset_y).perform()
        time.sleep(0.5)
        ac.release().perform()

    @staticmethod
    def get_track(distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正 2
                a = 2
            else:
                # 加速度为负 3
                a = -3
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    @staticmethod
    def move_slider_by_pid(browser, slider_button, offset_x, bg_width):
        track = get_pid_track(offset_x)
        # 避免拖动超过slider width
        track_list = [i for i in track if i > 0]
        max_index = max(range(len(track_list)), key=track_list.__getitem__)
        track_len = sum(track_list)
        if track_len > bg_width:
            num = track_len - bg_width
            track_len[max_index] -= num
            track.append(num)
        BaseSlider.move_slider_track(browser, slider_button, track)

    @staticmethod
    def move_slider_by_accelerated_speed(browser, slider_button, offset_x):
        track = BaseSlider.get_track(distance=offset_x)
        BaseSlider.move_slider_track(browser, slider_button, track)

    @staticmethod
    def move_slider(browser, slider_button, offset_x):
        action = webdriver.ActionChains(browser)
        # 拖动滑块
        action.click_and_hold(slider_button).move_by_offset(offset_x, 0)
        time.sleep(0.5)
        action.release().perform()
        BaseSlider.mouse_shake(browser)

    @staticmethod
    def mouse_shake(browser):
        """
        模拟释放鼠标手抖了一个机灵
        :return:
        """
        webdriver.ActionChains(browser).move_by_offset(xoffset=3, yoffset=0).perform()
        webdriver.ActionChains(browser).move_by_offset(xoffset=-3, yoffset=0).perform()
