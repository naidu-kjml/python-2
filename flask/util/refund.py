#-*-coding:utf-8 -*-
#author:xiaojiaming
import requests,json,time,logging
from decimal import Decimal, ROUND_HALF_UP

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
day = time.strftime("%Y%m%d")
handler = logging.FileHandler("log/refund/%s.txt"%day)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)
envs = {'0':'https://managetest.ruqimobility.com','1':'http://111.230.118.77'}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', "Content-Type":"application/json"}

def round(x):
	return Decimal(x).quantize(Decimal('.01'), ROUND_HALF_UP)

def login(env):
	logger.info('login ZT')
	headers1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
	session = requests.session()
	url = envs[env]+'/management/v1/login/web'
	if env == '0':
		data = {'username':'gactravel1','password':'ruqi123456','token':'123'}
	else:
		data = {'username':'gactravel','password':'qwe123!@#web','token':'123'}
	response = session.post(url, data=data, headers=headers1)
	logger.info(response.text)
	return session

def refund2(session,orderId,refundBaseAmount,refundExtraAmount,env):
	status = 0
	timestamp = int(time.time())
	payload = {"orderId":orderId,
	"comment":"网页脚本退款",
	"operator":"gactravel1",
	"timestamp":timestamp,
	"source":0,
	"payAmount":"7.1",
	"refundExtraAmount":refundExtraAmount,
	"refundBaseAmount":refundBaseAmount,
	"oid":'null'
	}
	url = envs[env]+'/management/v1/orderinfo/refund'
	logger.info('refund url:%s'%url)
	response = session.post(url, data=json.dumps(payload), headers=headers)
	if response.json()['code']==0:
		status = 1
	if response.json()['code']==110019:
		payload = {"orderId":orderId,
		"comment":"网页脚本退款",
		"operator":"gactravel1",
		"timestamp":timestamp,
		"source":0,
		"payAmount":"7.1",
		"refundExtraAmount":'0',
		"refundBaseAmount":'0.01',
		"oid":'null'
		}
		response = session.post(url, data=json.dumps(payload), headers=headers)
		if response.json()['code']==0:
			status = 2
	logger.info(response.text)
	return status
	
def getOrderId1(session,pageIndex,refundDays,userPhone,env):
	mes = '订单退款：\n'
	success_times = 0
	timestamp = int(time.time())
	#logger.info('**********pageIndex:%s************'%pageIndex)
	logger.info('****nomal refund****')
	createTime = 0
	payload = {"pageIndex":pageIndex,
		"pageSize":10,
		"userPhone":userPhone.strip(),
		"status":'9',
		"startTime":'null',
		"endTime":'null',
		"source":'null'}
	url = envs[env]+'/management/v1/orderinfo/queryListByFilter'
	logging.info('获取订单列表url:%s'%url)
	response = session.post(url, data=json.dumps(payload), headers=headers)
	if response.json()['code']!=0:
		logging.info(logger.info(response.text))
	orders = response.json()['content']['data']
	for order in orders:
		orderId = order['orderId']
		payDoneAmount = order['payDoneAmount'] #总支付
		refundBaseAmount = order['invoiceAmount'] #非附加费
		refundAmount = order['refundAmount'] #已退款金额
		createTime = int(time.mktime(time.strptime(order['createTime'], "%Y-%m-%d %H:%M:%S")))#创建时间
		#timePay = int(order['timePay']) # 支付时间
		refundExtraAmount = str(round(float(payDoneAmount))-round(float(refundBaseAmount))) #附加费
		if refundAmount==payDoneAmount:
			continue
		elif refundAmount<payDoneAmount:
			url = envs[env]+'/management/v1/orderinfo/query/%s?_=%d'%(orderId,timestamp)
			response = session.get(url, headers=headers)
			try:
				refundBaseAmount = response.json()['content']['showBaseAmount']
			except:
				logger.info(response.text)
			refundExtraAmount = response.json()['content']['showExtraAmount']
			logger.info('orderId：%s'%orderId)
			logger.info('payDoneAmount：%s refundBaseAmount：%s refundExtraAmount：%s'%(payDoneAmount,refundBaseAmount,refundExtraAmount))
			status = refund2(session,orderId,refundBaseAmount,refundExtraAmount,env)
			if status == 1:
				success_times = success_times+1
				mes = mes+'订单号：%s\n总费用：%s 非附加费：%s 附加费：%s\n'%(orderId,payDoneAmount,refundBaseAmount,refundExtraAmount)
			elif status == 2:
				success_times = success_times+1
				mes = mes+"订单号：%s\n订单费用：0.01\n"%orderId
		else:
			refundExtraAmount = str(round(float(payDoneAmount))-round(float(refundBaseAmount))) #附加费
			logger.info(orderId,payDoneAmount,refundBaseAmount,refundExtraAmount)
			status = refund2(session,orderId,refundBaseAmount,refundExtraAmount,env)
			if status == 1:
				success_times = success_times+1
				mes = mes+'订单号：%s\n总费用：%s 非附加费：%s 附加费：%s\n'%(orderId,payDoneAmount,refundBaseAmount,refundExtraAmount)
			elif status == 2:
				success_times = success_times+1
				mes = mes+"订单号：%s\n总费用：0.01\n"%orderId
	if timestamp-createTime<86400*refundDays:#判断订单时间
		getOrderId1(session,pageIndex+1,refundDays,userPhone,env)
	else:
		logger.info('nomal refund done!!!')
		print(success_times)
		if success_times==0:
			logging.info('No order need to be refunded')
			return "暂无订单需要退款"
		else:
			return mes

def getOrderId2(session,pageIndex,refundDays,userPhone,env):
	success_times = 0
	mes = '取消费退款：\n'
	timestamp = int(time.time())
	#logger.info('**********pageIndex:%s************'%pageIndex)
	logger.info('****cancelcost refund****')
	createTime = 0
	payload = {"pageIndex":pageIndex,
		"pageSize":10,
		"userPhone":userPhone.strip(),
		"status":'10',
		"startTime":'null',
		"endTime":'null',
		"source":'null'}
	url = envs[env]+'/management/v1/orderinfo/queryListByFilter'
	logging.info('url:%s'%url)
	response = session.post(url, data=json.dumps(payload), headers=headers)
	if response.json()['code']!=0:
		logging.info(logger.info(response.text))
	orders = response.json()['content']['data']
	for order in orders:
		orderId = order['orderId']
		payDoneAmount = order['payDoneAmount'] #总支付
		refundAmount = order['refundAmount'] #已退款金额
		createTime = int(time.mktime(time.strptime(order['createTime'], "%Y-%m-%d %H:%M:%S")))#创建时间
		#timePay = int(order['timePay']) # 支付时间
		refundBaseAmount = str(round(float(payDoneAmount))-round(float(refundAmount))) #附加费
		if refundAmount==payDoneAmount:
			continue
		else:
			logger.info('订单号：%s'%orderId)
			logger.info('支付费用：%s 退款取消费用：%s'%(payDoneAmount,refundBaseAmount))
			status = refund2(session,orderId,refundBaseAmount,0,env)
			if status == 1: 
				mes = mes+'订单号：%s\n订单费用：%s 退款取消费用：%s\n'%(orderId,payDoneAmount,refundBaseAmount)
				success_times = success_times+1
				logging.info("refund success times:%d"%success_times)
			elif status == 2:
				mes = mes+"订单号：%s\n订单费用：0.01\n"%orderId
				success_times = success_times+1
	if timestamp-createTime<86400*refundDays:#判断订单时间
		getOrderId2(session,pageIndex+1,refundDays,userPhone,env)
	else:
		logger.info('cancelcost refund done!!!')
		print(mes)
		if success_times==0:
			logging.info('No order need to be refunded')
			return "暂无取消费需要退款"
		else:
			return mes