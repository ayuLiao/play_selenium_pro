import json
import os
import time
import string
import zipfile

from selenium.webdriver.chrome.options import Options

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from proxy.proxy import *
from utils.ip_handler import *
from utils.user_agent import *
from configs import root_path
from logger import logger


class BaseBrowser:
    def __init__(self, options=None, browser=None):
        if options:
            self.options = options
        else:
            self.options = Options()
        self.browser = browser

    def wait_element(self, element_id, wait_time=15):
        try:
            WebDriverWait(self.browser, wait_time, 1).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except Exception as e:
            logger.error(f'[wait_element] 等待超时, error: {e}')
            raise

    def wait_element_css(self, css, wait_time=15):
        try:
            WebDriverWait(self.browser, wait_time, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css))
            )
        except Exception as e:
            logger.error(f'[wait_element_css] 等待超时, error: {e}')
            raise

    def add_header(self, headers):
        for k, v in headers.items():
            self.options.add_argument(f'{k}={v}')

    def load_cookies(self, url, cookies, refresh=False):
        """
        载入cookies，载入时，需要先放我对应的网站，否则无法正常载入cookies
        https://www.cnblogs.com/deliaries/p/14121204.html
        :param url: 加载cookies的url
        :param cookies: selenium.get_cookies() 获得的cookies对象
        :param refresh: 是否需要刷新页面
        :return:
        """
        self.browser.get(url)
        for c in cookies:
            self.browser.add_cookie(c)
        if refresh:
            self.browser.refresh()

    def disable_img_css(self):
        # 禁止图片
        prefs = {"profile.managed_default_content_settings.images": 2,
                 }
        self.options.add_experimental_option("prefs", prefs)

    def disable_css(self):
        # 禁止css加载
        prefs = {'permissions.default.stylesheet': 2}
        self.options.add_experimental_option("prefs", prefs)

    def browser_headless(self):
        # 无头浏览器
        self.options.add_argument('headless')

    def create_proxyauth_extension(self, proxy_host, proxy_port, proxy_username, proxy_password, scheme='http',
                                   plugin_path=None):
        """
        代理认证插件
        :param proxy_host: 代理地址或者域名（str类型）
        :param proxy_port: 代理端口号（int类型）
        :param proxy_username: 用户名（字符串）（私密代理）
        :param proxy_password: 密码 （字符串）（私密代理）
        :param scheme: 代理方式 默认http
        :param plugin_path:  扩展的绝对路径
        :return:
        """

        if plugin_path is None:
            plugin_path = 'vimm_chrome_proxyauth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return plugin_path

    def get_browser(self, disable_img=False, disable_css=False, headless=False, proxy_info=None, script_files=None):
        """
        获取浏览器对象
        :param disable_img: 是否禁用图片加载
        :param disable_css: 是否禁用CSS
        :param headless: 是否使用无头
        :param proxy_info: dict，是否使用代理
            proxy_info: {
                ip,
                port,
                username,
                password,
                type, 使用的代理类型
            }
        :param script_files: 需要前置执行的脚本
        :return:
        """

        # hidden webdriver feature
        self.options.add_argument("disable-blink-features=AutomationControlled")
        # open developer model, in this model, webdriver attribute is normal
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('lang=zh-CN,zh,zh-TW,en-US,en')

        user_agent = get_user_agent()
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

        self.add_header(headers)
        if headless:
            self.browser_headless()
        if disable_img:
            self.disable_img_css()
        if disable_css:
            self.disable_css()

        # set proxy
        if proxy_info:
            proxy_type = proxy_info.get('proxy_type', KYAIDAILI)
            if proxy_type == KYAIDAILI:
                # proxy need username and password, selenium need plug to supple this.
                # https://www.kuaidaili.com/doc/dev/sdk_http/#chrome
                proxyauth_plugin_path = self.create_proxyauth_extension(
                    proxy_host=f"{proxy_info['ip']}",  # proxy ip
                    proxy_port=f"{proxy_info['port']}",  # proxy port
                    proxy_username=f"{proxy_info['username']}",
                    proxy_password=f"{proxy_info['password']}"
                )
                self.options.add_extension(proxyauth_plugin_path)
            elif proxy_type == ZHIMA:
                ip = proxy_info['ip']
                port = proxy_info['port']
                proxy = f'{ip}:{port}'
                # PROXY = "23.23.23.23:3128" # IP:PORT or HOST:PORT
                self.options.add_argument('--proxy-server=%s' % proxy)

        path = os.path.join(root_path, 'chromedriver')
        browser = webdriver.Chrome(executable_path=path, chrome_options=self.options)

        defalut_script_files = [
            'stealth.min.js',  # hidden selenium feature
        ]
        if script_files:
            script_files.extend(defalut_script_files)
        else:
            script_files = defalut_script_files
        for sf in script_files:
            js_path = os.path.join(root_path, 'js', sf)
            with open(js_path, encoding='utf-8') as f:
                js = f.read()
            # execute javascript before webpage open
            browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js
            })

        if proxy_info:
            ip = proxy_info['ip']
            res_json = get_timezone_geolocation(ip)
            geo = {
                "latitude": res_json.get('lat', 116.480881),
                "longitude": res_json.get('lon', 39.989410),
                "accuracy": 1
            }
            # Default timezone is Shanghai
            tz = {
                "timezoneId": res_json.get('timezone', 'Asia/Shanghai')
            }
            browser.execute_cdp_cmd("Emulation.setGeolocationOverride", geo)
            browser.execute_cdp_cmd("Emulation.setTimezoneOverride", tz)

        browser.implicitly_wait(15)

        return browser
