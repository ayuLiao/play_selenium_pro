from proxy.kuaidaili import KuaiDaiLi
from proxy.zhima import ZhiMa

KYAIDAILI = 1
ZHIMA = 2


class Proxy:
    def __init__(self, kuaidaili_params=None, zhima_params=None, proxy_type=KYAIDAILI):
        """
        类型
        :param kuaidaili_params:
            order_id 订单号
            username 订单下的用户名（不同订单用户名不同）
            password 订单下的密码（不同订单密码不同）
            api_key 订单下的api_key
        :param zhima_params:

        :param proxy_type:
        """
        if kuaidaili_params:
            self.kuaidaili = KuaiDaiLi(**kuaidaili_params)
        if zhima_params:
            self.zhima = ZhiMa(**zhima_params)
        self.proxy_type = proxy_type

    def get_proxy_requests(self):
        """
        获得满足requests库格式的代理
        :return:
        """
        if self.proxy_type == KYAIDAILI:
            proxy = self.kuaidaili.get_dps()
            proxies = {
                "http": f"http://{self.kuaidaili.username}:{self.kuaidaili.password}@{proxy}/",
                "https": f"http://{self.kuaidaili.username}:{self.kuaidaili.password}@{proxy}/"
            }
            return proxies
        elif self.proxy_type == ZHIMA:
            proxy = self.zhima.get_proxy(num=1)
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}"
            }
            return proxies

    def get_proxy_selenium(self):
        """
        获得满足selenium库格式的代理
        :return:
        """
        if self.proxy_type == KYAIDAILI:
            proxy = self.kuaidaili.get_dps()
            proxy_info = {
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1],
                'username': self.kuaidaili.username,
                'password': self.kuaidaili.password
            }
            return proxy_info
        elif self.proxy_type == ZHIMA:
            proxy = self.zhima.get_proxy(num=1)
            proxy_info = {
                'ip': proxy.split(':')[0],
                'port': proxy.split(':')[1],
            }
            return proxy_info
