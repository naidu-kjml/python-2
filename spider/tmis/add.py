import requests

postData = {
	"version":"BR15N",
	"dll1":"windows",
	"dll2":"BR15N",
	"dll3":"长沙2号线",
	"dll4":"V1.0.0B2",
	"dll5":"2018-12-12",
	"dll6":1,
	"dll7":2,
	"dll8":3,
	"dll9":4,
	"dll10":5,
	"dll11":6,
	"column20":7
	}

cookies = {
	'JSESSIONID':'849271ABB41300EFFE03E1B0822CD06B',
	'login':'admin',
	'dlxm':''
	}

respon = requests.post('http://10.1.34.82:8081/tmis/dllAction!add.action',data=postData,cookies=cookies)
print(respon.text)