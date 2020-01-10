#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import requests
import json
import time
import logging
import pymysql

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


try:
    cnx = pymysql.connect(user='root', password='ruqi123456', host='10.10.28.121', database='xjming')
    cur = cnx.cursor()
except:
    print("数据库异常")

class Adjust:
    def __init__(self, user_phone, env='0', host='127.0.0.1'):
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.orders = []
        self.message = ''
        self.host = host

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
                   "operator": self.user_phone,
                   "orderId": orderId,
                   "timestamp": timestamp,
                   "source": 0}
        url = '%s/management/v1/adjust/charge' % self.url_top
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            self.message += "订单ID：%s\n改价成功!待支付金额为0\n" % orderId
            logger.info('Success')
            result = "改价成功"
        elif response.json()['code'] == 110029:
            self.message += "订单：%s\n%s\n" % (orderId, response.json()['message'])
            logger.info(response.json()['message'])
            result = response.json()['message']
        else:
            self.message += "订单：%s\n改价失败\n" % orderId
            logger.error(response.json()['message'])
            result = "改价失败：%s" % response.json()['message']
            # raise Exception
        # 数据库保存记录
        try:
            logger.info('Insert database')
            cur.execute(
                'insert into adjust_record (host,phone,orderId,result,time) values (%s, %s, %s, %s, %s)',
                [self.host, self.user_phone, orderId, result,
                 time.strftime("%Y-%m-%d %H:%M:%S")])
        except:
            logger.error("Insert Fail")

    def commit(self):
        start_times = time.time()
        logger.info("User phone:%s" % self.user_phone)
        self.login()
        self.get_orders()
        logger.info("The numbers of orders:%s" % len(self.orders))
        for order in self.orders:
            orderId = order['orderId']
            try:
                self.adjust(orderId)
            except:
                self.message += "订单：%s\n改价失败\n" % orderId
        try:
            logger.info("Database commit")
            cnx.commit()
        except:
            logger.error("Insert Fail")
        if len(self.orders) == 0:
            logger.info('No orders to be adjusted')
            self.message = "无待支付订单"
        else:
            costs_time = time.time() - start_times
            self.message += '\n改价完成\n耗时：%.2fs' % costs_time
        logger.info("Done!!!\n")


if __name__ == "__main__":
    start_time = time.time()
    for phone in USER_PHONE:
        try:
            AJ = Adjust(phone)
            AJ.commit()
        except:
            logger.error("Fail!!!")
    cost_time = time.time() - start_time
    logger.info("Cost time:%.2fs" % cost_time)
    time.sleep(3)
