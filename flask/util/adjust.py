#-*-coding:utf-8 -*-
import requests,json,time,logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
day = time.strftime("%Y%m%d")
handler = logging.FileHandler("log/adjust/%s.txt"%day)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)
envs = {'0':'https://managetest.ruqimobility.com','1':'http://111.230.118.77'}

def login(env):
	logger.info('登录中台')
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


def adjust2(session,orderId,env):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', "Content-Type":"application/json"}
	logger.info('改价')
	timestamp = int(time.time())
	payload = {"adjustBaseAmount":0,
		"adjustExtraAmount":0,
		"adjustComment":"网页脚本改价",
		"operator":"gactravel1",
		"orderId":orderId.strip(),
		"timestamp":timestamp,
		"source":0}
	url = envs[env]+'/management/v1/adjust/charge'
	response = session.post(url, data=json.dumps(payload), headers=headers)
	logger.info(response.text)
	logger.info('改价成功！！！')
	
def getOrderId(session,userPhone,env):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36', "Content-Type":"application/json"}
	logger.info('获取待支付订单')
	payload = {"pageIndex":1,
		"pageSize":10,
		"userPhone":userPhone.strip(),
		"status":'8',
		"startTime":'null',
		"endTime":'null',
		"source":'null'}
	url = envs[env]+'/management/v1/orderinfo/queryListByFilter'
	response = session.post(url, data=json.dumps(payload), headers=headers)
	orderId = response.json()['content']['data'][0]['orderId']
	logger.info(orderId)
	return orderId
