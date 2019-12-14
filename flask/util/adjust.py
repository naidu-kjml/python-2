# -*- coding:utf-8 -*-
# author:xiaojiaming

import requests
import json
import time

USER_PHONE = ['1325079029', '15989104405']
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}


class Adjust:
    def __init__(self, user_phone, env='0', logger_adjust=None):
        self.log = logger_adjust
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.orders = []
        self.message = ''

    def login(self):
        self.log.logger.info('Login RUQIMobility')
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '62.0.3202.89 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        url = '%s/management/v1/login/web' % self.url_top
        self.log.logger.debug(url)
        data = {'username': 'gactravel', 'password': 'qwe123!@#web', 'token': '123456'}
        response = self.session.post(url, data=data, headers=headers1)
        self.log.logger.debug(response.text)
        if response.json()['code'] == 0:
            self.log.logger.info('Login success')
        else:
            self.log.logger.error('Login fail!!!')
            self.log.logger.error(response.json()['message'])
            raise Exception

    def get_orders(self):
        self.log.logger.info('Get adjust orders')
        payload = {"pageIndex": 1,
                   "pageSize": 10,
                   "userPhone": self.user_phone.strip(),
                   "statusPay": "1",
                   "startTime": 'null',
                   "endTime": 'null',
                   "source": 'null'}
        url = '%s/management/v1/orderinfo/queryListByFilter' % self.url_top
        self.log.logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            self.log.logger.info('Success')
            self.orders = response.json()['content']['data']
        else:
            self.log.logger.error(response.json()['message'])
            raise Exception

    def adjust(self, orderId):
        self.log.logger.info('Adjust order:%s' % orderId)
        timestamp = int(time.time())
        payload = {"adjustBaseAmount": 0,
                   "adjustExtraAmount": 0,
                   "adjustComment": "网页脚本改价",
                   "operator": "gactravel1",
                   "orderId": orderId,
                   "timestamp": timestamp,
                   "source": 0}
        url = '%s/management/v1/adjust/charge' % self.url_top
        self.log.logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        self.log.logger.debug(response.text)
        if response.json()['code'] == 0:
            self.message += "订单：%s\n改价成功\n" % orderId
        else:
            self.message += "订单：%s\n改价失败\n" % orderId
            self.log.logger.error(response.json()['message'])
            raise Exception

    def commit(self):
        self.login()
        self.get_orders()
        self.log.logger.info("The numbers of orders:%s" % len(self.orders))
        if len(self.orders) == 0:
            self.log.logger.info('No orders to be adjusted')
            self.message = "无待支付订单"
        for order in self.orders:
            orderId = order['orderId']
            try:
                self.adjust(orderId)
            except:
                self.message += "订单：%s\n改价失败\n" % orderId
        self.log.logger.info("Done!!!\n")


if __name__ == "__main__":
    import logger
    log = logger.Loggers(filename="%s.log" % time.strftime("%Y%m%d"), level='info', log_dir='log\\adjust', dir_par_or_abs='par')
    for phone in USER_PHONE:
        AJ = Adjust(phone, logger_adjust=log)
        AJ.commit()
    time.sleep(5)
