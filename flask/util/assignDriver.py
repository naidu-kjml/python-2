#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import sys
import time
import pymysql
import requests
import json

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')

run_time = 180  # 持续时间 分钟
sleep_time = 5  # 查询间隔时间 秒
# client_phone = '13250790293'
# driver_phone = '15989104405'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}


class Assign:
    def __init__(self, client_phone, driver_phone, host='127.0.0.1'):
        self.client_phone = client_phone
        self.driver_phone = driver_phone
        self.session = requests.session()
        self.order = {}
        self.d = {}
        self.host = host

    def gen_sql_con(self):
        try:
            self.cnx = pymysql.connect(user='root', password='ruqi123456', host='10.10.28.121', database='xjming')
            self.cur = self.cnx.cursor()
        except:
            print("数据库异常")

    def clo_sql_con(self):
        try:
            self.cnx.commit()
            self.cur.close()
            self.cnx.close()
        except:
            print("数据库异常")

    def login(self):
        print('Login RUQIMobility')
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '62.0.3202.89 Safari/537.36',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        url = 'https://managetest.ruqimobility.com/management/v1/login/web'
        print(url)
        data = {'username': 'gactravel', 'password': 'qwe123!@#web', 'token': '123456'}
        response = self.session.post(url, data=data, headers=headers1)
        print(response.text)
        if response.json()['code'] == 0:
            print('Login success')
        else:
            print('Login fail!!!')
            print(response.json()['message'])
            raise Exception

    def get_orders(self):
        print('获取订单')
        payload = {"pageIndex": 1,
                   "pageSize": 5,
                   "userPhone": self.client_phone.strip(),
                   "startTime": 'null',
                   "endTime": 'null',
                   "source": 'null'}
        url = 'https://managetest.ruqimobility.com/management/v1/orderinfo/queryListByFilter'
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            try:
                self.order = response.json()['content']['data'][0]
            except:
                print('无订单')
                return False
            if self.order['status'] in [2, 3, 4, 5]:
                print('存在可改派的订单')
                if self.order['driverPhone'] != self.driver_phone:
                    print("满足指派条件")
                    return True
                else:
                    print("订单已被指定司机接单")
                    return False
            print("无派单中订单")
            return False
        else:
            print(response.json()['message'])
            return False

    def select_drivers(self):
        payload = {"pageIndex": 1,
                   "manualLimit": 10,
                   "carTypeIds": self.order['carTypeIds'],
                   "endCity": self.order['endCity'],
                   "orderId": self.order['orderId'],
                   "startCity": self.order['startCity'],
                   "startLatitude": self.order['startLatitude'],
                   "startLongitude": self.order['startLongitude'],
                   "productType": self.order['productTypeId'],
                   "startPosition": self.order['startPosition'],
                   "endPosition": self.order['endPosition']}
        url = 'https://managetest.ruqimobility.com/management/v1/orderAssign/selectDrivers'
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        print(response.text)
        if response.json()['code'] == 0:
            drivers = response.json()['content']
            if len(drivers) != 0:
                for driver in drivers:
                    if driver['phone'] == self.driver_phone:
                        print('获得指定司机信息')
                        self.d = {
                            "carId": driver['carId'],
                            "carTypeId": driver['carTypeId'],
                            "city": driver['city'],
                            "driverId": driver['driverId'],
                            "driverType": driver['driverType'],
                            "gender": driver['driverType'],
                            "name": driver['name'],
                            "phone": driver['phone'],
                            "carNumber": driver['carNumber'],
                            "color": driver['color'],
                            "carBrand": driver['carBrand'],
                            "carModel": driver['carModel'],
                            "carModelId": driver['carModelId']
                        }
                        return True
            else:
                print("无司机上线")
            return False
        else:
            print(response.json()['message'])
            return False

    def assign(self):
        print("指派中。。。")
        payload = {
            "productType": self.order['productTypeId'],
            "carTypeIds": self.order['carTypeIds'],
            "driverAssignList": [self.d],
            "endCity": self.order['endCity'],
            "orderId": self.order['orderId'],
            "startCity": self.order['startCity'],
            "startLatitude": self.order['startLatitude'],
            "startLongitude": self.order['startLongitude'],
            "startPosition": self.order['startPosition'],
            "endPosition": self.order['endPosition'],
            "endAdCode": self.order['endAdCode'],
            "startAdCode": self.order['startAdCode']
        }
        url = 'https://managetest.ruqimobility.com/management/v1/orderAssign/assignDriver'
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        print(response.text)
        if response.json()['code'] == 0:
            print('指派成功！！！')
            return True
        else:
            print(response.json()['message'])
            return False

    def commit(self):
        self.login()
        t = 1
        while t < int((run_time * 60) / sleep_time):
            print("******第%d次运行*****" % t)
            t += 1
            self.gen_sql_con()
            try:
                self.cur.execute('select * from assign where client_phone = %s and driver_phone = %s', (self.client_phone, self.driver_phone))
                status = self.cur.fetchall()[0][4]
            except:
                print('数据库异常')
                status = '0'
            self.clo_sql_con()
            print("查询当前状态为：", status)
            if status == '1':
                print("状态为解绑，停止运行")
                return
            if self.get_orders():
                for _ in range(5):
                    if self.select_drivers():
                        if self.assign():
                            t = 0
                            break
                    else:
                        print('指定司机未上线')
                        time.sleep(1)
            time.sleep(sleep_time)
        print('执行次数达到上限')
        return


if __name__ == "__main__":
    AS = Assign('15989104405', '13250790293')
    AS.commit()
