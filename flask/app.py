#-*-coding:utf-8 -*-
from flask import Flask, request, render_template
from util.mail import Email
from util.uploadDrivers import *
from util.adjust import *
from util.refund import *
import sys, json

reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)


@app.route('/uploadDrivers/',methods=['POST','GET'])
def uploadDrivers():
	return render_template('uploadDrivers.html')
	
@app.route('/adjust',methods=['POST','GET'])
def adjust():
	ip = request.remote_addr
	with open('data.json') as f:
		data = json.loads(f.read())
		try:
			phone = data[ip]
		except:
			phone = "请输入账号"
	return render_template('adjust.html',result=phone)

@app.route('/refund',methods=['POST','GET'])
def refund():
	ip = request.remote_addr
	with open('data.json') as f:
		data = json.loads(f.read())
		try:
			phone = data[ip]
		except:
			phone = "请输入账号"
	return render_template('refund.html',result=phone)

@app.route('/submit', methods=['POST'])
def submit():
	name = request.form.get('name') 
	phone = request.form.get('phone')
	city = request.form.get('city')
	env	= request.form.get('env')
	ip = request.remote_addr
	session = login(env)
	idcard_number = str(random.randint(111111, 999999)) + '199201010140'
	try:
		u = UD(session, name, phone, idcard_number, city, env)
		driver_id = u.commit()
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','司机录入')
		e.send("姓名：%s\n手机号：%s\n环境：%s\nIP：%s"%(name,phone,{'0':'测试环境',"1":"开发环境"}[env],ip))
		return {
			"code": "0", 
			"driver_id": driver_id
		}
	except:
		logger.exception("Failed to open sklearn.txt from logger.exception")
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','司机录入')
		e.send("录入失败！！！\n姓名：%s\n手机号：%s\n环境：%s\nIP：%s"%(name,phone,{'0':'测试环境',"1":"开发环境"}[env],ip))
		return {
			"code": "1"
		}

@app.route('/adjust1', methods=['POST'])
def adjust1():
	ip = request.remote_addr
	phone = request.form.get('phone')
	env	= request.form.get('env')
	logger.info('ENV：%s PHONE：%s'%({'0':'test',"1":"dev"}[env], phone))
	session = login(env)
	with open('data.json') as f:
		data = json.loads(f.read())
		data[ip] = phone
	with open('data.json','w') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)
	try:
		orderId = getOrderId(session,phone,env)
		adjust2(session,orderId,env)
		return {
			"code": "0",
			"orderId":orderId
		}
	except:
		return {
			"code": "1"
		}
	
@app.route('/refund1', methods=['POST'])
def refund1():
	ip = request.remote_addr
	phone = request.form.get('phone')
	env	= request.form.get('env')
	if env == '1':
		return {'code':"1","mes":"退款功能暂不支持开发环境"}
	logger.info('ENV：%s PHONE：%s'%({'0':'test',"1":"dev"}[env], phone))
	session = login(env)
	timestamp = int(time.time())
	with open('data.json') as f:
		data = json.loads(f.read())
		data[ip] = phone
	with open('data.json','w') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)
	print('退款账号：%s'%phone)
	try:
		mes1 = getOrderId1(session,1,1,phone.strip(),env)
		mes2 = getOrderId2(session,1,1,phone.strip(),env)
		return {
			"code": "0",
			"mes1":mes1,
			"mes2":mes2
		}
	except:
		return {
			"code": "1", 
			"mes":"退款失败"
		}


if __name__ == '__main__':
	app.run(host='0.0.0.0', port='5344', debug=True)
