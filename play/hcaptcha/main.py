import os
import time
import base64
import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from base_slider import BaseSlider
from base_browser import BaseBrowser
from utils.slide_crack import *
from utils.canvas import modify_random_canvas_js
from configs import root_path
from logger import logger


class HCaptchaBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        js_script_name = modify_random_canvas_js()
        self.browser = self.get_browser(script_files=[js_script_name])

    def run(self):
        """
        HCaptcha验证码
        """
        url = 'https://democaptcha.com/demo-form-eng/hcaptcha.html'
        self.browser.get(url)
        logs = self.browser.get_log("performance")
        events = self.process_browser_logs_for_network_events(logs)
        with open("log_entries.txt", "wt") as out:
            for event in events:
                pprint.pprint(event, stream=out)


