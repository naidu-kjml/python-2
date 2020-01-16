# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import sys
import time
import pymysql
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')

run_time = 1  # 持续时间 小时
sleep_time = 5  # 查询间隔时间 秒

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}


class Assign:
    def __init__(self):
        self.client_driver = {}
        self.session = requests.session()
        self.login()
        self.orders = []  # 订单列表
        self.clients = []
        self.drivers = []
        self.select_drivers = []  # 乘客、司机

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
        data = {'username': 'gactravel', 'password': 'qwe123!@#web', 'token': '123456'}
        for _ in range(5):
            response = self.session.post(url, data=data, headers=headers1)
            print(response.text)
            if response.json()['code'] == 0:
                print('Login success')
                return
            else:
                print('Login fail!!!')
                print(response.json()['message'])
            time.sleep(10)

    def get_orders(self):
        print('获取订单')
        payload = {"pageIndex": 1,
                   "pageSize": 10,
                   #  "userPhone": self.client_phone.strip(),
                   "startTime": 'null',
                   "endTime": 'null',
                   "source": 'null'}
        url = 'https://managetest.ruqimobility.com/management/v1/orderinfo/queryListByFilter'
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            self.orders = response.json()['content']['data']
            return True
        else:
            print(response.text)
            return False

    def select(self, order):
        payload = {"pageIndex": 1,
                   "manualLimit": 100,
                   "manualRadius": "2000",
                   "carTypeIds": order['carTypeIds'],
                   "endCity": order['endCity'],
                   "orderId": order['orderId'],
                   "startCity": order['startCity'],
                   "startLatitude": order['startLatitude'],
                   "startLongitude": order['startLongitude'],
                   "productType": order['productTypeId'],
                   "startPosition": order['startPosition'],
                   "endPosition": order['endPosition']}
        url = 'https://managetest.ruqimobility.com/management/v1/orderAssign/selectDrivers'
        for _ in range(5):
            response = self.session.post(url, data=json.dumps(payload), headers=headers)
            print(response.text)
            if response.json()['code'] == 0:
                self.select_drivers = response.json()['content']
                if len(self.select_drivers) != 0:
                    return True
                else:
                    print('无在线司机')
                    continue
            else:
                print('获取司机失败')
                continue
            time.sleep(0.1)
        return False

    def assign(self, order, driver_mes):
        print("指派中。。。")
        payload = {
            "productType": order['productTypeId'],
            "carTypeIds": order['carTypeIds'],
            "driverAssignList": [driver_mes],
            "endCity": order['endCity'],
            "orderId": order['orderId'],
            "startCity": order['startCity'],
            "startLatitude": order['startLatitude'],
            "startLongitude": order['startLongitude'],
            "startPosition": order['startPosition'],
            "endPosition": order['endPosition'],
            "endAdCode": order['endAdCode'],
            "startAdCode": order['startAdCode']
        }
        url = 'https://managetest.ruqimobility.com/management/v1/orderAssign/assignDriver'
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        print(response.text)
        if response.json()['code'] == 0:
            print('指派成功！！！')
            try:
                self.gen_sql_con()
                self.cur.execute(
                    'insert into assign_record (client_phone,driver_phone,order_id,time) values (%s, %s, %s, %s)',
                    [order["userPhone"], driver_mes["phone"], order['orderId'], time.strftime("%Y-%m-%d %H:%M:%S")])
                self.clo_sql_con()
            except:
                print('数据库异常')
            return True
        else:
            print(response.json()['message'])
            return False

    def get_client_diver(self):
        self.gen_sql_con()
        self.cur.execute('select * from assign where status=0')
        values = self.cur.fetchall()
        self.clo_sql_con()
        print(values)
        if len(values) == 0:
            print("不存在需绑定的账号")
            self.client_driver = {}
            self.clients = []
            self.drivers = []
            return False
        else:
            for v in values:
                self.client_driver[v[2]] = v[3]
                self.clients.append(v[2])
                self.drivers.append(v[3])
            return True

    def commit(self):
        t = 1
        while t < int((run_time * 3600) / sleep_time):
            print("******第%d次运行******" % t)
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            t += 1
            if self.get_client_diver():
                if self.get_orders():
                    for order in self.orders:
                        if order['status'] in [2, 3, 4, 5]:
                            print('存在可改派的订单')
                            if order['userPhone'] in self.clients and order['driverPhone'] != self.client_driver[order['userPhone']]:
                                print("满足指派条件")
                                if self.select(order):
                                    for driver in self.select_drivers:
                                        if driver['phone'] == self.client_driver[order['userPhone']]:
                                            driver_mes = {
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
                                            self.assign(order, driver_mes)
                                        else:
                                            print("司机未上线")
                                            continue
                                else:
                                    continue
                            else:
                                print('乘客不符合')
                                continue
                        else:
                            continue
            time.sleep(sleep_time)


class Email:
    def __init__(self, server, sender, password, receiver, title):
        self.title = title
        self.msg = MIMEMultipart('related')
        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def send(self, m):
        self.msg['Subject'] = Header(self.title, 'utf-8')
        self.msg['From'] = Header(self.sender)
        self.msg['To'] = self.receiver
        content = MIMEText(m, 'plain', 'utf-8')
        self.msg.attach(content)
        smtp_server = smtplib.SMTP(self.server)
        # smtp_server.set_debuglevel(1)
        smtp_server.starttls()
        smtp_server.login(self.sender, self.password)
        smtp_server.sendmail(self.sender, self.receiver, self.msg.as_string())
        smtp_server.close()


if __name__ == "__main__":
    try:
        AS = Assign()
        AS.commit()
    except:
        e = Email('smtp.qq.com', '981805032@qq.com', 'nmfavcrgtlfsbdeb', '13250790293@163.com', '派单绑定')
        e.send("绑定失败!!!")
