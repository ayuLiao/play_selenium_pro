import os

from dotenv import load_dotenv

from play.zapper.main import ZapperBrowser
from play.testGoogleV3.main import TestGoogleV3Browser
from play.ftx.main import FtxBrowser
from play.tradingeconomics.main import TradingeconomicsBrowser
from play.hcaptcha.main import HCaptchaBrowser
from play.jinshuju.main import JinshujuBrowser

from logger import logger

load_dotenv()


def zapper_play():
    for i in range(5):
        try:
            result = ZapperBrowser().get_grecaptcha()
            break
        except Exception as e:
            logger.error(f'第{i}次操作失败，重试中...,error: {e}', exc_info=True)
    print('结果: ', result)


def test_play():
    for i in range(5):
        try:
            result = TestGoogleV3Browser().get_grecaptcha()
            print('结果: ', result)
            break
        except Exception as e:
            logger.error(f'第{i}次操作失败，重试中..., error: {e}', exc_info=True)


def test_ftx():
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    ftx = FtxBrowser()
    cookies = ftx.login(email=email, password=password)
    ftx.browser.quit()
    print('login and get cookies: ', cookies)



def tradingeconomics_play():
    TradingeconomicsBrowser().run()

def hcaptcha_play():
    HCaptchaBrowser().run()

def jinshu_play():
    JinshujuBrowser().run()

if __name__ == '__main__':
    hcaptcha_play()
    # jinshu_play()