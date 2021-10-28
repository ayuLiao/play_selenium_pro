import requests

from logger import logger


class KuaiDaiLi:
    """快代理 https://www.kuaidaili.com/"""

    def __init__(self, username, password, order_id, api_key):
        """
        查看用户名与密码：https://www.kuaidaili.com/tps/genapiurl
        查看订单号与对应的api key：https://www.kuaidaili.com/usercenter/orderlist/
        :param username: 用户名
        :param password: 密码
        :param api_key: API KEY
        """
        self.username = username
        self.password = password
        self.order_id = order_id
        self.api_key = api_key
        self.session = requests.session()

    def get_order_info(self):
        """
        获取订单信息
        https://www.kuaidaili.com/doc/api/getorderinfo/
        :return:
        """
        url = f'https://dev.kdlapi.com/api/getorderinfo?orderid={self.order_id}&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            logger.error(f'[快代理] 获取当前隧道IP失败, err: {data}')
            raise
        return data.get('data', {})

    def get_tps_current_ip(self):
        """
        获得隧道IP
        https://www.kuaidaili.com/doc/api/tpscurrentip/
        :return:
        """
        url = f'https://tps.kdlapi.com/api/tpscurrentip?orderid={self.order_id}&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            logger.error(f'[快代理] 获取当前隧道IP失败, err: {data}')
            raise
        return data.get('data', {}).get('current_ip', '')

    def get_dps(self):
        """获得私密代理IP"""
        url = f'http://dps.kdlapi.com/api/getdps/?orderid={self.order_id}&num=1&pt=1&format=json&sep=1&signature={self.api_key}'
        r = self.session.get(url)
        data = r.json()
        if data.get('code', 0) != 0:
            logger.error(f'[快代理] 获取当前私密IP失败, err: {data}')
            raise
        proxy = data.get('data', {}).get('proxy_list')[0]
        return proxy
