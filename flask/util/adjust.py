#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import requests
import json
import time
import logging

USER_PHONE = ['13250790293', '15989104405']
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"} 

logger = logging.getLogger("log/adjust/%s.log" % time.strftime("%Y%m%d"))
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("log/adjust/%s.log" % time.strftime("%Y%m%d"), encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)


class Adjust:
    def __init__(self, user_phone, env='0'):
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.orders = []
        self.message = ''

    def login(self):
        logger.info('Login RUQIMobility')
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '62.0.3202.89 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        url = '%s/management/v1/login/web' % self.url_top
        logger.debug(url)
        data = {'username': 'gactravel', 'password': 'qwe123!@#web', 'token': '123456'}
        response = self.session.post(url, data=data, headers=headers1)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info('Login success')
        else:
            logger.error('Login fail!!!')
            logger.error(response.json()['message'])
            raise Exception

    def get_orders(self):
        logger.info('Get adjust orders')
        payload = {"pageIndex": 1,
                   "pageSize": 10,
                   "userPhone": self.user_phone.strip(),
                   "statusPay": "1",
                   "startTime": 'null',
                   "endTime": 'null',
                   "source": 'null'}
        url = '%s/management/v1/orderinfo/queryListByFilter' % self.url_top
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            logger.info('Success')
            self.orders = response.json()['content']['data']
        else:
            logger.error(response.json()['message'])
            raise Exception

    def adjust(self, orderId):
        logger.info('Adjust order:%s' % orderId)
        timestamp = int(time.time())
        payload = {"adjustBaseAmount": 0,
                   "adjustExtraAmount": 0,
                   "adjustComment": "网页脚本改价",
                   "operator": "gactravel1",
                   "orderId": orderId,
                   "timestamp": timestamp,
                   "source": 0}
        url = '%s/management/v1/adjust/charge' % self.url_top
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            self.message += "订单：%s\n改价成功\n" % orderId
        elif response.json()['code'] == 110029:
            self.message += "订单：%s\n%s\n" % (orderId, response.json()['message'])
        else:
            self.message += "订单：%s\n改价失败\n" % orderId
            logger.error(response.json()['message'])
            raise Exception

    def commit(self):
        logger.info("User phone:%s" % self.user_phone)
        self.login()
        self.get_orders()
        logger.info("The numbers of orders:%s" % len(self.orders))
        if len(self.orders) == 0:
            logger.info('No orders to be adjusted')
            self.message = "无待支付订单"
        for order in self.orders:
            orderId = order['orderId']
            try:
                self.adjust(orderId)
            except:
                self.message += "订单：%s\n改价失败\n" % orderId
        logger.info("Done!!!\n")


if __name__ == "__main__":
    for phone in USER_PHONE:
        try:
            AJ = Adjust(phone)
            AJ.commit()
        except:
            logger.error("Fail!!!")
    time.sleep(5)
