#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

from importlib import reload
from flask import Flask, request, render_template
from util.mail import Email
from util.uploadDrivers import *
from util.adjust import Adjust
from util.refund import Refund
from util.logger import Loggers
import sys
import json

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')
app = Flask(__name__)

log_adjust = Loggers(filename="%s.log" % time.strftime("%Y%m%d"), level='debug', log_dir='flask\\log\\adjust',
                     dir_par_or_abs='par')
log_refund = Loggers(filename="%s.log" % time.strftime("%Y%m%d"), level='debug', log_dir='flask\\log\\refund',
                     dir_par_or_abs='par')


@app.route('/uploadDrivers/', methods=['POST', 'GET'])
def uploadDrivers():
    return render_template('uploadDrivers.html')


@app.route('/adjust', methods=['POST', 'GET'])
def adjust():
    ip = request.remote_addr
    with open('data.json') as f:
        data = json.loads(f.read())
        try:
            phone = data[ip]
        except:
            phone = "请输入账号"
    return render_template('adjust.html', result=phone)


@app.route('/refund', methods=['POST', 'GET'])
def refund():
    ip = request.remote_addr
    with open('data.json') as f:
        data = json.loads(f.read())
        try:
            phone = data[ip]
        except:
            phone = "请输入账号"
    return render_template('refund.html', result=phone)


@app.route('/testutil/uploadDrivers/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    city = request.form.get('city')
    env = request.form.get('env')
    ip = request.remote_addr
    session = login(env)
    idcard_number = str(random.randint(111111, 999999)) + '199201010140'
    try:
        u = UD(session, name, phone, idcard_number, city, env)
        driver_id = u.commit()
        msg = "录入成功\n司机ID:%d" % driver_id
        e = Email('smtp.qq.com', '981805032@qq.com', 'nmfavcrgtlfsbdeb', '13250790293@163.com', '司机录入')
        e.send("姓名：%s\n手机号：%s\n环境：%s\nIP：%s" % (name, phone, {'0': '测试环境', "1": "开发环境"}[env], ip))
        return {
            "code": "0",
            "msg": msg
        }

    except:
        logger.exception("Failed to open sklearn.txt from logger.exception")
        e = Email('smtp.qq.com', '981805032@qq.com', 'nmfavcrgtlfsbdeb', '13250790293@163.com', '司机录入')
        e.send("录入失败！！！\n姓名：%s\n手机号：%s\n环境：%s\nIP：%s" % (name, phone, {'0': '测试环境', "1": "开发环境"}[env], ip))
        return {
            "code": "1",
            "msg": "录入失败"
        }


@app.route('/testutil/adjust/submit', methods=['POST'])
def adjust1():
    ip = request.remote_addr
    phone = request.form.get('phone')
    env = request.form.get('env')
    log_adjust.logger.info('ENV:%s PHONE:%s IP:%s' % ({'0': 'test', "1": "dev"}[env], phone, ip))
    with open('data.json') as f:
        data = json.loads(f.read())
        data[ip] = phone
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    try:
        A = Adjust(phone, env, logger_adjust=log_adjust)
        A.commit()
        return {
            "code": "0",
            "msg": A.message
        }
    except:
        return {
            "code": "1",
            "msg": "改价失败"
        }


@app.route('/testutil/refund/submit', methods=['POST'])
def refund1():
    ip = request.remote_addr
    phone = request.form.get('phone')
    env = request.form.get('env')
    if env == '1':
        return {'code': "1", "msg": "退款功能暂不支持开发环境"}
    log_refund.logger.info('ENV:%s PHONE:%s IP:%s' % ({'0': 'test', "1": "dev"}[env], phone, ip))
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        data[ip] = phone
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    try:
        RF: Refund = Refund(env=env, user_phone=phone, logger_refund=log_refund)
        RF.commit()
        return {
            "code": "0",
            "msg": RF.message
        }
    except:
        return {
            "code": "1",
            "msg": "退款失败"
        }
    finally:
        del RF


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5344')
    app.run(host='0.0.0.0', port='5344', debug=True)
