#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

from decimal import Decimal, ROUND_HALF_UP
import requests
import json
import time
import sys
import logging
import pymysql

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')

USER_PHONE = ['13250790293', '15989104405']
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}

logger = logging.getLogger("log/refund/%s.log" % time.strftime("%Y%m%d"))
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("log/refund/%s.log" % time.strftime("%Y%m%d"), encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)


def round(x):
    return Decimal(x).quantize(Decimal('.01'), ROUND_HALF_UP)


class Refund:
    def __init__(self, env='0', refund_days=1, user_phone=None, host='127.0.0.1'):
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.timestamp = int(time.time())
        self.refund_days = refund_days
        self.refund_success_times = 0
        self.orders = []
        self.message = ''
        self.host = host
        try:
            self.cnx = pymysql.connect(user='root', password='ruqi123456', host='10.10.28.121', database='xjming')
            self.cur = self.cnx.cursor()
        except:
            print("数据库异常")

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

    def get_orders(self, pageIndex=1):
        logger.info("Get refund orders")
        logger.debug("Page %d" % pageIndex)
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
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            logger.info('Success')
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])
            raise Exception
        orders = response.json()['content']['data']
        self.orders = self.orders + orders
        createTime = int(time.mktime(time.strptime(orders[-1]['createTime'], "%Y-%m-%d %H:%M:%S")))  # 订单创建时间
        logger.debug(createTime)
        if self.timestamp - createTime < 86400 * self.refund_days:  # 判断订单时间
            logger.debug("Get next page")
            self.get_orders(pageIndex + 1)
        else:
            logger.debug('Finish')

    def get_order_info(self, orderId):
        logger.debug('Get order info')
        url = '%s/management/v1/orderinfo/query/%s?_=%d' % (self.url_top, orderId, self.timestamp)
        logger.debug(url)
        response = self.session.get(url, headers=headers)
        if response.json()['code'] == 0:
            refundBaseAmount = response.json()['content']['showBaseAmount']
            refundExtraAmount = response.json()['content']['showExtraAmount']
            payRecords = response.json()['content']['payRecords']
            return refundBaseAmount, refundExtraAmount, payRecords
        else:
            logger.error(response.json()['message'])
            raise Exception

    def refund(self, orderId, payDoneAmount, refundBaseAmount, refundExtraAmount):
        logger.info('Commit refund')
        logger.info('refundBaseAmount:%s,refundExtraAmount:%s' % (refundBaseAmount, refundExtraAmount))
        payload = {"orderId": orderId,
                   "comment": "网页脚本退款",
                   "operator": self.user_phone,
                   "timestamp": self.timestamp,
                   "source": 0,
                   "payAmount": payDoneAmount,
                   "refundExtraAmount": refundExtraAmount,
                   "refundBaseAmount": refundBaseAmount,
                   "oid": 'null'
                   }
        url = '%s/management/v1/orderinfo/refund' % self.url_top
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.info(response.text)
        if response.json()['code'] == 0:
            self.refund_success_times += 1
            result = "退款成功"
            self.message = self.message + '订单ID:%s\n 支付金额:%s 非附加费:%s 附加费:%s\n' % (
                orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
            logger.info("Refund Success!!!")
        else:
            result = "退款失败：%s" % response.json()['message']
            logger.error(response.json()['message'])
        # 数据库保存记录
        try:
            logger.info('Insert database')
            self.cur.execute(
                'insert into refund_record (host,phone,orderId,refundBaseAmount,refundExtraAmount,result,time) values (%s, %s, %s, %s, %s, %s, %s)',
                [self.host, self.user_phone, orderId, refundBaseAmount, refundExtraAmount, result,
                 time.strftime("%Y-%m-%d %H:%M:%S")])
        except:
            logger.error("Insert Fail")

    def commit(self):
        starts_time = time.time()
        logger.info("user phone:%s" % self.user_phone)
        self.login()
        logger.info('Refund days:%s' % self.refund_days)
        try:
            self.get_orders()
        except IndexError as e:
            self.message = "暂无订单需退款"
            logger.error(e)
            logger.error('No order to refunded')
            return
        logger.info('Order_Numbers:%d' % len(self.orders))
        for order in self.orders:
            orderId = order['orderId']
            payDoneAmount = order['payDoneAmount']  # 总支付
            if order['statusRefund'] != 3 and float(payDoneAmount) != 0:  # 非完全退款
                refundBaseAmount, refundExtraAmount, payRecords = self.get_order_info(orderId)
                logger.debug('OrderID：%s\n payDoneAmount:%s refundBaseAmount:%s refundExtraAmount:%s' % (
                    orderId, payDoneAmount, refundBaseAmount, refundExtraAmount))
                logger.debug(payRecords)
                if float(refundBaseAmount) != 0 or float(refundExtraAmount) != 0:
                    pay_times = 0
                    pay_amount = 0
                    refund_sum = 0
                    for pay_record in payRecords:
                        logger.debug(pay_record['payStatus'])
                        logger.debug(pay_record['payAmount'])
                        if pay_record['payStatus'] == 2:  # 支付记录
                            pay_times += 1
                            if pay_amount <= pay_record['payAmount']:
                                pay_amount = pay_record['payAmount']
                        elif pay_record['payStatus'] == 3:  # 退款记录
                            refund_sum += round(float(pay_record['payAmount']))
                    logger.debug('pay_times: %s' % pay_times)
                    logger.debug(str(refund_sum))
                    if pay_times == 1:  # 普通订单
                        logger.info('OrderID:%s\n payDoneAmount:%s refundBaseAmount:%s refundExtraAmount:%s' % (
                            orderId, payDoneAmount, refundBaseAmount, refundExtraAmount))
                        self.refund(orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
                    elif pay_times == 0:  # 对公订单
                        logger.debug('订单ID:%s 对公订单无需退款\n' % orderId)
                    else:  # 预支付订单
                        if refund_sum < pay_amount:
                            pay_amount = round(pay_amount) - refund_sum
                            if float(refundBaseAmount) >= pay_amount:
                                self.refund(orderId, payDoneAmount, str(pay_amount), '0')
                                self.refund(orderId, payDoneAmount,
                                            str(round(float(refundBaseAmount)) - pay_amount),
                                            refundExtraAmount)
                            else:
                                self.refund(orderId, payDoneAmount, refundBaseAmount,
                                            str(pay_amount - round(float(refundBaseAmount))))
                                self.refund(orderId, payDoneAmount, '0', str(round(float(refundExtraAmount)) - (
                                        pay_amount - round(float(refundBaseAmount)))))
                        else:
                            self.refund(orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
                else:
                    logger.debug('Order has been adjusted to 0')  # 改价订单，无需退款
            else:
                logger.debug("Order has been refunded or adjusted to 0")  # 完全退款订单
        if self.refund_success_times == 0:
            self.message = "暂无订单需退款"
        else:
            costs_time = time.time() - starts_time
            self.message += "\n退款完成\n耗时：%.2fs" % costs_time
        try:
            logger.info("Database commit")
            self.cnx.commit()
            self.cur.close()
            self.cnx.close()
        except:
            logger.error("Insert Fail")
        finally:
            logger.info("Refund %d orders" % self.refund_success_times)
            logger.info("Done!!!\n")


if __name__ == "__main__":
    start_time = time.time()
    for phone in USER_PHONE:
        try:
            RF = Refund(user_phone=phone)
            RF.commit()
        except:
            print('Refund fail')
    cost_time = time.time() - start_time
    logger.info('Cost time:%.2fs' % cost_time)
    time.sleep(3)
