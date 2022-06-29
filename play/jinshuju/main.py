import time
from selenium.webdriver.chrome.options import Options

from base_browser import BaseBrowser
from logger import logger
from selenium.webdriver.common.by import By


class JinshujuBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        self.browser = self.get_browser()

    def run(self):
        url = 'https://jinshuju.net/f/wqnVAP'
        btn_xpath = '/html/body/div[2]/div/div[3]/a'
        self.browser.get(url)
        self.browser.find_element(by=By.XPATH, value=btn_xpath).click()
        time.sleep(5)
        input_xpath = '//*[@id="root"]/div/form/div[3]/div[1]/div[16]/div/div/div[2]/div[1]/div/span/span/input'
        self.browser.find_element(by=By.XPATH, value=input_xpath).send_keys('xxx')
        time.sleep(5)
