import requests,re
from bs4 import BeautifulSoup

cookies = {
	'JSESSIONID':'F2C7E168255E8A2BD325D2069AFD46DC',
	'login':'admin',
	'dlxm':''
	}

respon = requests.post('http://10.1.34.82:8081/tmis/softAction!datagrid.action',cookies=cookies)
print(respon.json())

a = respon.json()['rows']
for i in a:
	print(i['oanumber'])