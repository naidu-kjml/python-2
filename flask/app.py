#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xiaojiaming'

from flask import Flask, request, render_template
from util.sql import Sql
from util.mail import Email
from util.uploadDrivers import *
from util.adjust import Adjust
from util.refund import Refund
import sys

citys = {'440100': '广州', '440300': '深圳', '110000': '北京', '441900': '东莞'}

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')
app = Flask(__name__)


@app.route('/uploadDrivers/', methods=['POST', 'GET'])
def uploadDrivers():
    return render_template('uploadDrivers.html')


@app.route('/assign/', methods=['POST', 'GET'])
def assign():
    ip = request.remote_addr
    try:
        values = Sql.select_assign1(ip)
        if len(values) == 0:
            client_phone = "请输入乘客手机号"
            driver_phone = "请输入司机手机号"
        else:
            client_phone = values[-1][2]
            driver_phone = values[-1][3]
    except:
        e = Email('smtp.qq.com', '981805032@qq.com', 'nmfavcrgtlfsbdeb', '13250790293@163.com', '派单绑定')
        e.send("数据库异常")
        print("数据库异常")
        client_phone = "请输入乘客手机号"
        driver_phone = "请输入司机手机号"
    return render_template('assign.html', client_phone=client_phone, driver_phone=driver_phone)


@app.route('/adjust', methods=['POST', 'GET'])
def adjust():
    ip = request.remote_addr
    try:
        values = Sql.select_user(ip)
        if len(values) == 0:
            phone = "请输入账号"
        else:
            phone = values[-1][2]
    except:
        print("数据库异常")
        phone = "请输入账号"
    return render_template('adjust.html', result=phone)


@app.route('/refund', methods=['POST', 'GET'])
def refund():
    ip = request.remote_addr
    try:
        values = Sql.select_user(ip)
        if len(values) == 0:
            phone = "请输入账号"
        else:
            phone = values[-1][2]
    except:
        print("数据库异常")
        phone = "请输入账号"
    return render_template('refund.html', result=phone)


@app.route('/testutil/uploadDrivers/submit', methods=['POST'])
def submit():
    start_time = time.time()
    name = request.form.get('name').strip()
    phone = request.form.get('phone').strip()
    city = request.form.get('city').strip()
    env = request.form.get('env').strip()
    ip = request.remote_addr
    if len(phone) != 11:
        return {
            "code": "1",
            "msg": '请输入正确的手机号！'
        }
    if len(name) == 0 or len(name) > 11:
        return {
            "code": "1",
            "msg": '请输入正确的司机姓名！'
        }
    try:
        u = UD(name, phone, city, env)
        u.commit()
        result = '成功'
        try:
            print("Insert database")
            Sql.insert_dr(ip, name, phone, citys[city], {'0': '测试环境', "1": "开发环境"}[env], result,
                          time.strftime("%Y-%m-%d %H:%M:%S"))
            print("Success")
        except:
            print("Fail!!!")
        cost_time = time.time() - start_time
        message = '%s\n耗时：%.2fs' % (u.message, cost_time)
        return {
            "code": "0",
            "msg": message
        }
    except:
        e = Email('smtp.qq.com', '981805032@qq.com', 'nmfavcrgtlfsbdeb', '13250790293@163.com', '司机录入')
        e.send("录入失败！！！\n姓名：%s\n手机号：%s\n环境：%s\nIP：%s" % (name, phone, {'0': '测试环境', "1": "开发环境"}[env], ip))
        result = '失败'
        try:
            print("Insert database")
            Sql.insert_dr(ip, name, phone, citys[city], {'0': '测试环境', "1": "开发环境"}[env], result,
                          time.strftime("%Y-%m-%d %H:%M:%S"))
            print('Success')
        except:
            print("Fail!!!")
        return {
            "code": "1",
            "msg": "录入失败"
        }


@app.route('/testutil/adjust/submit', methods=['POST'])
def adjust1():
    ip = request.remote_addr
    phone = request.form.get('phone').strip()
    env = request.form.get('env')
    #  log.logger.info('ENV:%s PHONE:%s IP:%s' % ({'0': 'test', "1": "dev"}[env], phone, ip))
    try:
        values = Sql.select_user(ip)
        if len(values) == 0:
            Sql.insert_user(ip, phone, time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            Sql.update_user(ip, phone, time.strftime("%Y-%m-%d %H:%M:%S"))
    except:
        print('数据库异常')
    try:
        A = Adjust(phone, env, host=ip)
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
    phone = request.form.get('phone').strip()
    env = request.form.get('env')
    if len(phone) != 11:
        return {
            "code": "1",
            "msg": '请输入正确的手机号！'
        }
    if env == '1':
        return {'code': "1", "msg": "退款功能暂不支持开发环境"}
    #  logger.info('ENV:%s PHONE:%s IP:%s' % ({'0': 'test', "1": "dev"}[env], phone, ip))
    try:
        values = Sql.select_user(ip)
        if len(values) == 0:
            Sql.insert_user(ip, phone, time.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            Sql.update_user(ip, phone, time.strftime("%Y-%m-%d %H:%M:%S"))
    except:
        print("数据库异常")
    try:
        RF = Refund(env=env, user_phone=phone, host=ip)
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


@app.route('/testutil/assign/submit', methods=['POST'])
def assign1():
    ip = request.remote_addr
    client_phone = request.form.get('client_phone').strip()
    driver_phone = request.form.get('driver_phone').strip()
    status = request.form.get('status')
    try:
        values = Sql.select_assign(client_phone)
    except:
        print("数据库异常")
        values = ''
    if status == '0':  # 绑定
        if len(values) == 0:
            try:
                Sql.insert_assign(ip, client_phone, driver_phone, status, time.strftime("%Y-%m-%d %H:%M:%S"))
                return {
                    "code": "0",
                    "msg": "绑定成功"
                }
            except:
                print("数据库异常")
                return {
                    "code": "1",
                    "msg": "绑定失败"
                }
        else:
            is_driver_exist = False
            for v in values:
                driver_sql = v[3]
                if driver_phone == driver_sql:
                    is_driver_exist = True
                    try:
                        Sql.update_assign(ip, client_phone, driver_phone, '0', time.strftime("%Y-%m-%d %H:%M:%S"))
                    except:
                        print('数据库异常')
                else:
                    try:
                        Sql.update_assign(ip, client_phone, driver_sql, '1', time.strftime("%Y-%m-%d %H:%M:%S"))
                    except:
                        print('数据库异常')
            if not is_driver_exist:
                try:
                    Sql.insert_assign(ip, client_phone, driver_phone, status, time.strftime("%Y-%m-%d %H:%M:%S"))
                except:
                    print("数据库异常")
            return {
                "code": "0",
                "msg": "绑定成功"
            }
    elif status == '1':
        if len(values) == 0:
            try:
                Sql.insert_assign(ip, client_phone, driver_phone, status, time.strftime("%Y-%m-%d %H:%M:%S"))
            except:
                print('数据库异常')
            return {
                "code": "0",
                "msg": "未绑定过该账号"
            }
        else:
            try:
                Sql.update_assign(ip, client_phone, driver_phone, status, time.strftime("%Y-%m-%d %H:%M:%S"))
            except:
                print('数据库异常')
            return {
                "code": "0",
                "msg": "解绑成功"
            }
    else:
        return {
            "code": "1",
            "msg": "type字段错误"
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5344', debug=True)
