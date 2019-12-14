#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

from importlib import reload
import requests
import json
import time
import re
import sys


if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')
USER_PHONE = ['13250790292', '15989104405']
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}


class Refund:
    def __init__(self, env='0', refund_days=1, user_phone=None, logger_refund=None):
        self.log = logger_refund
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.timestamp = int(time.time())
        self.refund_days = refund_days
        self.refund_success_times = 0
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

    def get_orders(self, pageIndex=1):
        self.log.logger.info("Get refund orders")
        self.log.logger.debug("Page %d" % pageIndex)
        if self.user_phone:
            payload = {"pageIndex": pageIndex,
                       "pageSize": 10,
                       "userPhone": self.user_phone.strip(),
                       "statusPay": '3',
                       "startTime": 'null',
                       "endTime": 'null',
                       "source": 'null'}
        else:
            payload = {"pageIndex": pageIndex,
                       "pageSize": 10,
                       "statusPay": '3',
                       "startTime": 'null',
                       "endTime": 'null',
                       "source": 'null'}
        url = '%s/management/v1/orderinfo/queryListByFilter' % self.url_top
        self.log.logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            self.log.logger.info('Success')
        else:
            self.log.logger.error('Fail!!!')
            self.log.logger.error(response.json()['message'])
            raise Exception
        orders = response.json()['content']['data']
        self.orders = self.orders + orders
        createTime = int(time.mktime(time.strptime(orders[-1]['createTime'], "%Y-%m-%d %H:%M:%S")))  # 订单创建时间
        self.log.logger.debug(createTime)
        if self.timestamp - createTime < 86400 * self.refund_days:  # 判断订单时间
            self.log.logger.debug("Get next page")
            self.get_orders(pageIndex + 1)
        else:
            self.log.logger.debug('Finish')

    def get_order_info(self, orderId):
        self.log.logger.debug('Get order info')
        url = '%s/management/v1/orderinfo/query/%s?_=%d' % (self.url_top, orderId, self.timestamp)
        self.log.logger.debug(url)
        response = self.session.get(url, headers=headers)
        self.log.logger.debug(response.text)
        if response.json()['code'] == 0:
            refundBaseAmount = response.json()['content']['showBaseAmount']
            refundExtraAmount = response.json()['content']['showExtraAmount']
            return refundBaseAmount, refundExtraAmount
        else:
            self.log.logger.error(response.json()['message'])
            raise Exception

    def refund(self, orderId, payDoneAmount, refundBaseAmount, refundExtraAmount):
        self.log.logger.info('Commit refund')
        payload = {"orderId": orderId,
                   "comment": "网页脚本退款",
                   "operator": "gactravel1",
                   "timestamp": self.timestamp,
                   "source": 0,
                   "payAmount": payDoneAmount,
                   "refundExtraAmount": refundExtraAmount,
                   "refundBaseAmount": refundBaseAmount,
                   "oid": 'null'
                   }
        url = '%s/management/v1/orderinfo/refund' % self.url_top
        self.log.logger.info(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        self.log.logger.debug(response.text)
        if response.json()['code'] == 0:
            self.refund_success_times += 1
            self.message = self.message + '订单ID:%s\n 支付金额:%s 非附加费:%s 附加费:%s\n' % (
                orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
            self.log.logger.info("Refund Success!!!")
        elif response.json()['code'] == 110019 and response.json()['message'] != '退款失败：订单号不存在':  # 兼容预付费情况
            try:
                res = re.match('.*?支付记录1:(.*?):支付记录2:(.*?)元', response.json()['message'])
                self.log.logger.debug(res.group(1), res.group(2))
                if int(refundBaseAmount) == 0:
                    self.refund(orderId, payDoneAmount, '0', res.group(1))
                    self.refund(orderId, payDoneAmount, '0', res.group(2))
                elif int(refundExtraAmount) == 0:
                    self.refund(orderId, payDoneAmount, res.group(1), '0')
                    self.refund(orderId, payDoneAmount, res.group(2), '0')
                else:
                    self.self.log.logger.error('%s Refund fail!!!' % orderId)
                    self.message += '订单ID:%s\n退款失败\n' % orderId
            except:
                self.message += '订单ID:%s\n退款失败\n' % orderId
                self.self.log.logger.error('%s Refund fail!!!' % orderId)
        else:
            self.log.logger.error(response.json()['message'])
            raise Exception

    def commit(self):
        self.login()
        if self.user_phone:
            self.log.logger.info("Refund phone:%s" % self.user_phone)
        self.log.logger.info('Refund days:%s' % self.refund_days)
        try:
            self.get_orders()
        except IndexError as e:
            self.message = "暂无订单需退款"
            self.log.logger.error(e)
            self.log.logger.error('No order to refunded')
            return
        self.log.logger.info('Order_Numbers:%d' % len(self.orders))
        for order in self.orders:
            orderId = order['orderId']
            payDoneAmount = order['payDoneAmount']  # 总支付
            if order['statusRefund'] != 3:  # 非完全退款
                refundBaseAmount, refundExtraAmount = self.get_order_info(orderId)
                self.log.logger.debug('OrderID：%s\n payDoneAmount:%s refundBaseAmount:%s refundExtraAmount:%s' % (
                    orderId, payDoneAmount, refundBaseAmount, refundExtraAmount))
                if int(refundBaseAmount) != 0 or int(refundExtraAmount) != 0:
                    self.log.logger.info('OrderID：%s\n payDoneAmount:%s refundBaseAmount:%s refundExtraAmount:%s' % (
                        orderId, payDoneAmount, refundBaseAmount, refundExtraAmount))
                    self.refund(orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
                else:
                    self.log.logger.debug('Order has been adjusted to 0')  # 改价订单，无需退款
            else:
                self.log.logger.debug("Order has been refunded")  # 完全退款订单
            time.sleep(0.1)
        if self.refund_success_times == 0:
            self.message = "暂无订单需退款"
        self.log.logger.info("Refund %d orders" % self.refund_success_times)
        self.log.logger.info("Done!!!\n")


if __name__ == "__main__":
    import logger
    log = logger.Loggers(filename="%s.log" % time.strftime("%Y%m%d"), level='info', log_dir='log\\refund', dir_par_or_abs='par')
    for phone in USER_PHONE:
        try:
            RF = Refund(user_phone=phone, logger_refund=log)
            RF.commit()
        except:
            print('Refund fail')
    time.sleep(5)
