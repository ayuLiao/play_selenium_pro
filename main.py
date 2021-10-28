from play.zapper.main import ZapperBrowser
from play.test.main import TestBrowser

from logger import logger

def zapper_play():
    for i in range(5):
        try:
            result = ZapperBrowser().get_grecaptcha()
            break
        except Exception as e:
            logger.error(f'第{i}次操作失败，重试中...,error: {e}')
    print('结果: ', result)

def test_play():
    for i in range(5):
        try:
            result = TestBrowser().get_grecaptcha()
            print('结果: ', result)
            break
        except Exception as e:
            logger.error(f'第{i}次操作失败，重试中...')


if __name__ == '__main__':
    test_play()