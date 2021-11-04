import os
import time
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from base_slider import BaseSlider
from base_browser import BaseBrowser
from utils.slide_crack import *
from utils.canvas import modify_random_canvas_js
from configs import root_path
from logger import logger


class FtxBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        js_script_name = modify_random_canvas_js()
        self.browser = self.get_browser(script_files=[js_script_name])

    def slider_handler(self):
        # 滑块图片
        slider_css = 'body > div.geetest_holder.geetest_mobile.geetest_ant.geetest_popup > div.geetest_popup_box > div.geetest_popup_wrap > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute'
        self.wait_element_css(slider_css, wait_time=10)
        slider_img_path = BaseSlider.save_base64_img(browser=self.browser, css=slider_css, img_name='slider.png')
        # 背景图片
        bg_css = 'body > div.geetest_holder.geetest_mobile.geetest_ant.geetest_popup > div.geetest_popup_box > div.geetest_popup_wrap > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_bg.geetest_absolute'
        self.wait_element_css(bg_css, wait_time=10)
        bg_img_path = BaseSlider.save_base64_img(browser=self.browser, css=bg_css, img_name='bg.png')
        bg_width = int(self.browser.find_element(by=By.CSS_SELECTOR, value=bg_css).get_attribute('width'))

        sc = SlideCrack(slider_img_path, bg_img_path, '')
        offset_x = sc.discern()
        slider_button_css = 'body > div.geetest_holder.geetest_mobile.geetest_ant.geetest_popup > div.geetest_popup_box > div.geetest_popup_wrap > div.geetest_wrap > div.geetest_slider.geetest_ready > div.geetest_slider_button'
        slider_button = self.browser.find_element(by=By.CSS_SELECTOR, value=slider_button_css)
        BaseSlider.move_slider_by_pid(browser=self.browser,
                                      slider_button=slider_button,
                                      offset_x=offset_x - 5,
                                      bg_width=bg_width)
        time.sleep(2)

    def login(self, email, password):
        url = 'https://ftx.com/'
        self.browser.get(url)
        dialog_css = 'body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div'
        self.wait_element_css(css=dialog_css, wait_time=5)
        self.browser.find_element(by=By.CSS_SELECTOR,
                                  value='body > div.MuiDialog-root > div.MuiDialog-container.MuiDialog-scrollPaper > div > div.MuiDialogActions-root.MuiDialogActions-spacing > button').click()

        register_css = '#root > div > header > div > div > div.jss696 > button'
        self.wait_element_css(css=register_css, wait_time=10)
        self.browser.find_element(by=By.CSS_SELECTOR, value=register_css).click()
        self.browser.find_element(by=By.CSS_SELECTOR, value="#email").send_keys(email)
        self.browser.find_element(by=By.CSS_SELECTOR, value="#confirmPassword").send_keys(email)
        self.browser.find_element(by=By.CSS_SELECTOR, value="#password").send_keys(password)

        form_element = self.browser.find_element(by=By.TAG_NAME, value="form")
        slider_check_button = form_element.find_element(by=By.TAG_NAME,
                                                        value="div > div > div:nth-child(6) > div > div > div.geetest_btn > div.geetest_radar_btn > div.geetest_radar_tip")
        slider_check_button.click()
        time.sleep(2)
        # 尝试5次
        for i in range(5):
            if slider_check_button.accessible_name == 'Verification Succeeded':
                break
            self.slider_handler()
            try:
                refresh_css = "body > div.geetest_holder.geetest_mobile.geetest_ant.geetest_popup > div.geetest_popup_box > div.geetest_popup_wrap > div.geetest_panel > div > a.geetest_refresh_1"
                self.wait_element_css(css=refresh_css, wait_time=5)
                self.browser.find_element(by=By.CSS_SELECTOR, value=refresh_css).click()
            except:
                if slider_check_button.accessible_name == 'Verification Succeeded':
                    break

        form_element.find_element(by=By.CSS_SELECTOR,
                                  value='div > div > div:nth-child(7) > label > span.MuiButtonBase-root.MuiIconButton-root.jss734.MuiCheckbox-root.MuiCheckbox-colorSecondary.MuiIconButton-colorSecondary > span.MuiIconButton-label > input').click()
        time.sleep(0.5)
        form_element.find_element(by=By.CSS_SELECTOR, value='div > div > div:nth-child(9) > button').click()
        logger.info(f'email: {email} login success! Wait for the browser to load the login cookies.')
        time.sleep(5)
        cookies = self.browser.get_cookies()
        return cookies
