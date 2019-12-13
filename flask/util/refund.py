# -*-coding:utf-8 -*-
# author:xiaojiaming
from importlib import reload
import requests
import json
import time
import re
import sys

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')
USER_PHONE = ['13250790293', '15989104405']
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}


class Refund:
    def __init__(self, env='0', refund_days=1, user_phone=None):
        self.url_top = envs[env]
        self.user_phone = user_phone
        self.session = requests.session()
        self.login()
        self.timestamp = int(time.time())
        self.refund_days = refund_days
        self.refund_success_times = 0
        self.orders = []
        self.message = ''

    def login(self):
        print('Login ruqimobility')
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '62.0.3202.89 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        url = '%s/management/v1/login/web' % self.url_top
        print(url)
        data = {'username': 'gactravel', 'password': 'qwe123!@#web', 'token': '123456'}
        response = self.session.post(url, data=data, headers=headers1)
        print(response.text)

    def get_orders(self, pageIndex=1):
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
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        orders = response.json()['content']['data']
        self.orders = self.orders + orders
        createTime = int(time.mktime(time.strptime(orders[-1]['createTime'], "%Y-%m-%d %H:%M:%S")))  # 订单创建时间
        if self.timestamp - createTime < 86400 * self.refund_days:  # 判断订单时间
            self.get_orders(pageIndex + 1)

    def get_order_info(self, orderId):
        print('Get order info')
        url = '%s/management/v1/orderinfo/query/%s?_=%d' % (self.url_top, orderId, self.timestamp)
        print(url)
        response = self.session.get(url, headers=headers)
        refundBaseAmount = response.json()['content']['showBaseAmount']
        refundExtraAmount = response.json()['content']['showExtraAmount']
        return refundBaseAmount, refundExtraAmount

    def refund(self, orderId, payDoneAmount, refundBaseAmount, refundExtraAmount):
        print('Commit refund')
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
        print(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        print(response.text)
        if response.json()['code'] == 0:
            self.refund_success_times += 1
            self.message = self.message + '订单ID:%s\n 支付金额:%s 非附加费:%s 附加费:%s\n' % (
                    orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
            print("Refund Success!!!")
        if response.json()['code'] == 110019 and response.json()['message'] != '退款失败：订单号不存在':  # 兼容预付费情况
            try:
                res = re.match('.*?支付记录1:(.*?):支付记录2:(.*?)元', response.json()['message'])
                print(res.group(1), res.group(2))
                if int(refundBaseAmount) == 0:
                    self.refund(orderId, payDoneAmount, '0', res.group(1))
                    self.refund(orderId, payDoneAmount, '0', res.group(2))
                elif int(refundExtraAmount) == 0:
                    self.refund(orderId, payDoneAmount, res.group(1), '0')
                    self.refund(orderId, payDoneAmount, res.group(2), '0')
                else:
                    print('%s Refund fail!!!' % orderId)
            except:
                self.message += '订单ID:%s\n退款失败' % orderId
                print('%s Refund fail!!!' % orderId)

    def commit(self):
        if self.user_phone:
            print("Refund phone:%s" % self.user_phone)
        print('Refund days:%s' % self.refund_days)
        self.get_orders()
        print('Order_Numbers:%d' % len(self.orders))
        for order in self.orders:
            orderId = order['orderId']
            payDoneAmount = order['payDoneAmount']  # 总支付
            if order['statusRefund'] != 3:  # 非完全退款
                refundBaseAmount, refundExtraAmount = self.get_order_info(orderId)
                print('OrderID：%s\n payDoneAmount:%s refundBaseAmount:%s refundExtraAmount:%s' % (
                    orderId, payDoneAmount, refundBaseAmount, refundExtraAmount))
                if int(refundBaseAmount) != 0 or int(refundExtraAmount) != 0:  # 非改价订单
                    self.refund(orderId, payDoneAmount, refundBaseAmount, refundExtraAmount)
                else:
                    print('Order has been adjusted to 0')  # 改价订单，无需退款
            else:
                pass  # 完全退款订单
            time.sleep(0.1)
        if self.refund_success_times == 0:
            self.message = "暂无订单需退款"
        print("Refund %d orders" % self.refund_success_times)
        print("Done!!!")


if __name__ == "__main__":
    for phone in USER_PHONE:
        RF = Refund(user_phone=phone)
        RF.commit()
        print(RF.message)
    time.sleep(5)
