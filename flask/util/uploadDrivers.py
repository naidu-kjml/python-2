#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

import time
import requests
import json
import random
import logging
from faker import Faker

# *********配置信息********
# citys = {'广州':'440100', '深圳':'440300', '北京':'110000','东莞':'441900'}
envs = {'0': 'https://managetest.ruqimobility.com', '1': 'http://111.230.118.77'}
rentCompanyIds = {'440100': '608', '440300': '625', '110000': '637', '441900': '639'}
faker = Faker('zh_CN')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
    "Content-Type": "application/json"}

logger = logging.getLogger("log/uploadDrivers/%s.log" % time.strftime("%Y%m%d"))
logger.setLevel(level=logging.DEBUG)
handler = logging.FileHandler("log/uploadDrivers/%s.log" % time.strftime("%Y%m%d"), encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(console)


class UD:
    def __init__(self, name, phone, city, env):
        self.url_top = envs[env]
        self.session = requests.session()
        self.name = name
        self.phone = phone
        self.idCardNumber = str(random.randint(111111, 999999)) + '199201010140'
        self.city = city
        self.env = envs[env]
        self.driverId = ''
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
        logger.debug(data)
        response = self.session.post(url, data=data, headers=headers1)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info('Login success')
        else:
            logger.error('Login fail!!!')
            logger.error(response.json()['message'])
            raise Exception

    def upload(self):
        logger.info('Generate new account')
        logger.info(self.phone)
        url = self.env + '/management/v1/driver/recruit/create'
        logger.debug(url)
        payload = {
            'city': self.city,
            'currentResidentialAddress': faker.address(),
            'drivingAge': '0',
            'gender': '1',
            'idCardNumber': self.idCardNumber,
            'isCertificateA': 'True',
            'licenseType': 'C2',
            'name': self.name,
            'nativePlace': faker.address(),
            'phone': self.phone,
            'recruitComment': '123',
            'recruitmentChannels': '1'
        }
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info('Success')
            self.driverId = response.json()['content']['driverId']
            logger.info('Driver id:%s' % self.driverId)
        elif response.json()['code'] == 150001:
            logger.info('Driver ID exist!!!')
            logger.info('Get driver ID')
            url = self.env + '/management/v1/driver/recruit/list'
            logger.debug(url)
            payload = {"pageIndex": 1, "pageSize": 10, "name": None, "gender": None, "phone": self.phone,
                       "recruitmentChannels": None, "city": None, "licenseType": None, "drivingAge": None,
                       "isCertificateA": None, "auditStatus": None}
            response = self.session.post(url, data=json.dumps(payload), headers=headers)
            logger.debug(response.text)
            try:
                self.driverId = response.json()['content']['data'][0]['driverId']
                logger.info('Driver ID：%d' % self.driverId)
            except:
                logger.info('Fail!!!')
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def interview(self):
        # 邀请面试
        logger.info('Interview')
        url = self.env + '/management/v1/driver/recruit/notice/interview/%s?_=1569383098574' % self.driverId
        logger.debug(url)
        response = self.session.get(url, headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        elif response.json()['code'] == 150011:
            logger.info("Has been interviewed before")
            logger.error(response.json()['message'])
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])
        # 面试
        payload = {"driverId": self.driverId,
                   "driverAddress": "使用测试脚本添加",
                   "nation": "汉",
                   "driverHeight": "111",
                   "driverWeight": "123",
                   "driverEducation": "高中",
                   "driverResidentType": "1",
                   "driverMaritalStatus": "已婚",
                   "presentFamilyAddress": "",
                   "emergencyContact": "13250890999",
                   "emergencyContactPhone": "13284884374",
                   "licenseNumber": "112121",
                   "getDriverLicenseDate": 1569340800,
                   "licenseStartDate": 1569340800,
                   "licenseEndDate": 1664121600,
                   "certificateA": self.idCardNumber,
                   "networkCarIssueDate": 1569340800,
                   "getNetworkCarProofDate": 1569340800,
                   "networkCarProofOn": 1569340800,
                   "networkCarProofOff": 1664121600,
                   "email": "",
                   "result": 'true',
                   "interviewDate": 1569340800,
                   "interviewComment": "备注",
                   "interviewData": "6834389/05f28172-64b1-4e00-80ed-b87df99711431569394421373.png"}
        url = self.env + '/management/v1/driver/recruit/interview/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.json()['code'] == 0:
            logger.info("Success")
        elif response.json()['code'] == 150011:
            logger.info("Has been interviewed before")
            logger.error(response.json()['message'])
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def roadtest(self):
        logger.info('Road test')
        url = self.env + '/pages/driver/driver_recruitment_add.html?driverId=%s&tabId=tab3&status=3' % self.driverId
        logger.debug(url)
        self.session.get(url, headers=headers)

        payload = {"driverId": self.driverId,
                   "result": 'true',
                   "roadTestDate": 1569340800,
                   "roadTestComment": "备注",
                   "roadTestData": "6834388/549335f2-8a0d-4964-b05f-8336078e96ce1569396922197.png"
                   }
        url = self.env + '/management/v1/driver/recruit/roadTest/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        elif response.json()['code'] == 150011:
            logger.info("Has been tested before")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def train(self):
        logger.info('Train')
        url = self.env + '/pages/driver/driver_recruitment_add.html?driverId=%s&tabId=tab4&status=4' % self.driverId
        logger.debug(url)
        self.session.get(url, headers=headers)

        payload = {"driverId": self.driverId,
                   "result": 'true',
                   "courseDate": 1569340800,
                   "trainComment": "备注",
                   "courseData": "6834389/3ce2d860-fdf1-4f78-bd67-523cf69497661569397241370.png"
                   }
        url = self.env + '/management/v1/driver/recruit/train/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        elif response.json()['code'] == 150011:
            logger.info("Has been trained before")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def recruit(self):
        logger.info('Recruit')
        url = self.env + '/pages/driver/driver_recruitment_add.html?driverId=%s&tabId=tab5&status=5' % self.driverId
        logger.debug(url)
        self.session.get(url, headers=headers)

        payload = {"driverId": self.driverId,
                   "isPayDeposit": 1,
                   "depositPayDate": 1569340800,
                   "depositPayAmt": "100",
                   "depositPayType": 1,
                   "signDate": 1569340800,
                   "materialReceivingInstructions": "说明",
                   "informationArchives": "6834388/1078de38-8752-45fd-aba0-4fdfb66746a51569397594363.zip"
                   }
        url = self.env + '/management/v1/driver/recruit/sign/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        elif response.json()['code'] == 150011:
            logger.info("Has been recruited before")
            logger.error(response.json()['message'])
        else:
            logger.info('Fail!!!')
            logger.error(response.json()['message'])

    def img(self):
        logger.info('Upload driver img')
        payload = {"driverId": self.driverId,
                   "headImg": "https://travel-driverdev-driverpub-1258234669.cos.ap-guangzhou.myqcloud.com/6834282/c14358e9-babb-41a3-bebf-6d9cfb0560c11570786304009.png",
                   "driverImg": "6834396/55b3910d-695a-495e-8dfb-e38968d963811569405148143.png",
                   "idCardImgFront": "6834396/02b1d99e-7245-4fad-a267-1076d7f29d5c1569405154540.png",
                   "idCardImgBack": "6834396/ac648cb1-5ff7-4aa6-84e4-6825075aefa91569405158969.png",
                   "idCardImgHold": "6834396/bb7f3494-3103-487b-9d9e-9ef4c675920e1569405162164.png",
                   "licenseImg": "6834396/a1893c64-bf6b-4751-87ce-51216abb41221569405166250.png",
                   "licenseImgBack": "6834396/4c6f8fa4-8067-47e0-91aa-b696e1ef0f871569405171499.png"}
        url = self.env + '/management/v1/driver/recruit/img/uploadImg'
        logger.debug(url)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.debug("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def contract(self):
        logger.info('Contract')
        payload = {"driverId": self.driverId,
                   "contractPhoto": "6834396/fdb895e1-77a9-4a6c-83d7-6fa9e7a17d501569405655930.pdf",
                   "operator": "gactravel1", "contractStatus": "YX", "contractType": "HT", "invalidTime": 1569427200,
                   "signTime": 1569340800, "type": "ZC", "validTime": 1569340800}
        url = self.env + '/management/v1/driver/contract/update'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.debug("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def cource(self):
        logger.info('Cource')
        payload = {"courseDate": 1569340800, "courseName": "测试", "driverId": self.driverId, "duration": 86400,
                   "operator": "gactravel1", "type": "GQ", "startTime": 1569340800, "stopTime": 1569427200,
                   "trainingAccountInfo": "6834396/9e82e1ab-df17-42ec-922f-18abff91e4c01569405966360.png",
                   "trainerName": "测试"}
        url = self.env + '/management/v1/driver/cource/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.debug("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def base(self):
        logger.info('Upload all driver message')
        payload = {"driverId": self.driverId,
                   "idCardNumber": self.idCardNumber,
                   "licenseNumber": self.idCardNumber,
                   "driverType": "",
                   "licenseType": "C2",
                   "email": "981805021@qq.com",
                   "name": self.name,
                   "gender": "1",
                   "city": self.city,
                   "licenseEndDate": 1664121600,
                   "licenseStartDate": 1569340800,
                   "labourCompanyId": "327",
                   "birthDate": 694198800000,
                   "nation": "汉",
                   "driverHeight": "180",
                   "driverWeight": "70",
                   "appVersion": "1.6",
                   "commercialType": "1",
                   "driverAddress": "该司机使用脚本添加!!!",
                   "driverResidentType": "1",
                   "driverContactAddress": "广州市",
                   "driverEducation": "本科",
                   "nativePlace": faker.address(),
                   "licensePhotoId": "111111",
                   "recruitmentChannels": "1",
                   "driverMaritalStatus": "已婚",
                   "certificateA": self.idCardNumber,
                   "emergencyContact": "13250890999",
                   "emergencyContactPhone": "13284884374",
                   "getDriverLicenseDate": 1569340800,
                   "getNetworkCarProofDate": 1569340800,
                   "mobileModel": "Android",
                   "mapType": "1",
                   "netType": "3",
                   "presentFamilyAddress": "",
                   "networkCarIssueDate": 1664121600,
                   "networkCarIssueOrganization": "1312213231",
                   "networkCarProofOff": 1569427200,
                   "networkCarProofOn": 1569340800,
                   "operator": "gactravel1",
                   "taxiDriver": "1",
                   "informationArchives": "6834396/25320fd7-4c71-4d6e-80ef-2e5e835a03621569406462272.zip"}
        url = self.env + '/management/v1/driver/base/info/update'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def createCar(self):
        # 获取租赁公司id
        # logger.info('新建车辆')
        # payload = {"pageIndex":1,
        # "pageSize":11,
        # "city":self.city}
        # url = 'https://managetest.ruqimobility.com/management/v1/carrent/list'
        # response = self.session.post(url, data=json.dumps(payload), headers=headers)
        # logger.info(response.text)
        # rentCompanyId = response.json()['content']['data'][0]['rentCompanyId']
        logger.info("Create car")
        rentCompanyId = rentCompanyIds[self.city]
        carNumber = '粤AB' + str(random.randint(10000, 99999))
        engineNumber = str(random.randint(1111111111, 9999999999))
        carVerifyCode = str(random.randint(11111111111111111, 99999999999999999))
        carCertNo = str(random.randint(1111111111, 9999999999))
        logger.debug('Car message:%s,%s,%s,%s,%s' % (rentCompanyId, carNumber, engineNumber, carCertNo, carVerifyCode))
        payload = {"carAttributeId": "300027", "carLicenseImg": "", "carImgs": "", "carNumber": carNumber,
                   "carNumberImg": "", "carVerifyCode": carVerifyCode, "city": self.city, "engineNumber": engineNumber,
                   "oilWear": "6", "rentCompanyId": rentCompanyId, "variableBox": "1", "totalMileage": "12121",
                   "plateColor": "3", "carCertNo": carCertNo}
        url = self.env + '/management/v1/vehicle/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])
        self.carId = response.json()['content']['carId']
        payload = {"carId": self.carId, "vehicleType": "2", "ownerName": "1", "transAgency": "1",
                   "transDateStart": 1570665600, "transDateStop": 1665360000, "certifyDateB": 1570665600, "fixState": 1,
                   "nextFixDate": 1665360000, "checkDate": 1665360000, "checkState": 2, "feelogger.infoid": "1",
                   "feePrintid": "1111111", "gpsBrand": "1", "gpsModel": "1", "gpsImei": "1", "commercialType": 3,
                   "fareType": "1", "vehicleTec": "1", "gpsInstallDate": 1570665600, "vehicleSafe": "1",
                   "certifyDateA": 1570665600}
        url = self.env + '/management/v1/vehicle/ext/create'
        logger.debug(url)
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])

    def setcar(self):
        # 获取车辆列表
        logger.info('Set car')
        url = self.env + '/management/v1/driver/setCar'
        logger.debug(url)
        payload = {"driverId": self.driverId, "carId": self.carId, "listenCarTypes": "1", "operator": "gactravel1"}
        logger.debug(payload)
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        logger.debug(response.text)
        if response.json()['code'] == 0:
            logger.info("Success")
            self.message = '录入成功! 司机ID:%s' % self.driverId
        else:
            logger.error('Fail!!!')
            logger.error(response.json()['message'])
            self.message = "录入失败!!!"

    def commit(self):
        self.login()
        self.upload()
        self.interview()
        self.roadtest()
        self.train()
        self.recruit()
        self.img()
        self.contract()
        self.cource()
        self.base()
        self.createCar()
        self.setcar()

