import time
from selenium.webdriver.chrome.options import Options

from base_browser import BaseBrowser
from utils.canvas import modify_random_canvas_js
from logger import logger

class TestBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        js_script_name = modify_random_canvas_js()
        # self.browser = self.get_browser(headless=True, script_files=[js_script_name])
        self.browser = self.get_browser()

    def get_grecaptcha(self):
        url = 'http://ayuliaotest.com/'
        self.browser.get(url)
        logger.info('页面加载完成')
        code = '6LfjvvwcAAAAANdSZE0jSI4s3kFqNpA1KywTElS0'
        js_script = '''
        return await window.grecaptcha.execute('{code}', {action: 'claimQuesRewards'}).then(function(data){return data})
        '''.replace('{code}', code)
        result = self.browser.execute_script(js_script)
        logger.info('执行js成功')
        return result
