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


class TradingeconomicsBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        js_script_name = modify_random_canvas_js()
        self.browser = self.get_browser(script_files=[js_script_name])

    def run(self):
        """
        获取网页中的svg
        svg存放内嵌的iframe中，iframe加载需要科学上网
        """
        url = 'https://tradingeconomics.com/commodity/baltic'
        self.browser.get(url)
        iframe = self.browser.find_element(by=By.CSS_SELECTOR, value="#trading_chart").find_element(by=By.TAG_NAME, value='iframe')
        self.browser.switch_to.frame(iframe)
        time.sleep(10)
        svg_button_xpath = '//*[@id="widget-container"]/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[7]/div'
        svg_button = self.browser.find_element(by=By.XPATH, value=svg_button_xpath).click()


