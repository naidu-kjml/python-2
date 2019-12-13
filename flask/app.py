# -*-coding:utf-8 -*-
# author:xiaojiaming
from flask import Flask, request, render_template
from util.mail import Email
from util.uploadDrivers import *
from util.adjust import *
from util.refund import Refund
import sys
import json

if 'linux' in sys.platform:
    reload(sys)
    sys.setdefaultencoding('utf8')
app = Flask(__name__)


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
    logger.info('ENV：%s PHONE：%s' % ({'0': 'test', "1": "dev"}[env], phone))
    session = login(env)
    with open('data.json') as f:
        data = json.loads(f.read())
        data[ip] = phone
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    try:
        orderId = getOrderId(session, phone, env)
        adjust2(session, orderId, env)
        msg = '改价成功\n订单ID：' + orderId
        return {
            "code": "0",
            "msg": msg
        }
    except:
        return {
            "code": "1",
            "msg": "暂无待支付订单"
        }


@app.route('/testutil/refund/submit', methods=['POST'])
def refund1():
    ip = request.remote_addr
    phone = request.form.get('phone')
    env = request.form.get('env')
    if env == '1':
        return {'code': "1", "msg": "退款功能暂不支持开发环境"}
    logger.info('ENV：%s PHONE：%s' % ({'0': 'test', "1": "dev"}[env], phone))
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        data[ip] = phone
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    try:
        RF: Refund = Refund(env=env, user_phone=phone)
        RF.commit()
    except:
        return {
            "code": "1",
            "msg": "退款失败"
        }
    return {
        "code": "0",
        "msg": RF.message
    }


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5344')
    app.run(host='0.0.0.0', port='5344', debug=True)
