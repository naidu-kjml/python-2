import requests

postData = {
	'diqu':'',
	'xianlu':'',
	'sblx':'mokuai',
	'bbh':'banbenhao',
	'tjrq':'tjriqi',
	'oanumber':'oa',
	'status':'zhuangtai',
	'tester':'ceshirenyuan',
	'plantime':'jhwcsj',
	'nowtime':'sjwcsj',
	'testresult':'csjg',
	'column20':''
	}

cookies = {
	'JSESSIONID':'849271ABB41300EFFE03E1B0822CD06B',
	'login':'admin',
	'dlxm':''
	}

respon = requests.post('http://10.1.34.82:8081/tmis/softAction!add.action',data=postData,cookies=cookies)
print(respon.text)