import time

import requests

from logger import logger


class ZhiMa:
    """芝麻代理 https://www.zhimaruanjian.com/"""

    def __init__(self):
        self.app_key = ''
        self.session = requests.session()

    def get_proxy(self, num, pro=0, city=0):
        """
        获得代理ip
        :param num: 代理ip数量
        :param pro: 省份, 440000 广东省
        :param city: 城市, 440100 广州市
        :return:
        """
        # 直连IP
        url = f'http://webapi.http.zhimacangku.com/getip?num={num}&type=2&pro={pro}&city=0&yys=0&port=1&time=2&ts=1&ys=1&cs=1&lb=1&sb=0&pb=4&mr=1&regions='
        proxy_info = None
        for i in range(5):
            r = self.session.get(url)
            proxy_info = r.json()
            code = proxy_info.get('code', 0)
            if code == 113:
                # 请添加白名单 x.x.x.x
                # 将ip添加到代理提供商的白名单服务中
                ip = proxy_info.get('msg').replace('', '')
                self.add_whitelist(ip)
                logger.info(f'{ip}添加进白名单, proxy_info: {proxy_info}')
            elif code == 111:
                # 请2秒后再试
                sleep_time = proxy_info.get('msg')[1]
                time.sleep(int(sleep_time))
                logger.info(f'获取代理IP太频繁，proxy_info: {proxy_info}')
            elif code == 0:
                break
        if not proxy_info:
            raise
        proxy_data = proxy_info.get('data')
        proxy_data = proxy_data[0]
        proxy = proxy_data['ip'] + ':' + str(proxy_data['port'])
        return proxy

    def add_whitelist(self, ip):
        """
        添加到白名单 - 非白名单IP无法使用代理IP
        :param ip:
        :return:
        """
        url = f'https://wapi.http.linkudp.com/index/index/save_white?neek=326117&appkey={self.app_key}&white={ip}'
        r = requests.get(url)
        return r.json()
