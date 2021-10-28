import time
from selenium.webdriver.chrome.options import Options

from base_browser import BaseBrowser
from logger import logger

class ZapperBrowser(BaseBrowser):

    def __init__(self):
        self.options = Options()
        self.browser = self.get_browser()

    def get_grecaptcha(self):
        url = 'https://zapper.fi/zh'
        self.browser.get(url)
        for i in range(3):
            js_script = '''
                var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; 
                var network = performance.getEntries() || {}; 
                return network;
                '''
            networks = self.browser.execute_script(js_script)
            data = [n['name'] for n in networks if 'www.google.com/recaptcha/enterprise.js' in n.get('name', '')]
            if data:
                break
            time.sleep(5)
        if not data:
            logger.error('没有从network中找到code，重试')
            raise
        data = data[0]
        code = data.split('=')[-1]
        js_script = '''
        return await window.grecaptcha.execute('{code}', {action: 'claimQuesRewards'}).then(function(data){return data})
        '''.replace('{code}', code)
        result = self.browser.execute_script(js_script)
        return result


