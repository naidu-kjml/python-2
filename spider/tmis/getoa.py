import requests,re
from bs4 import BeautifulSoup

cookies = {
	'JSESSIONID': 'AA44EA56E2C53DA2733C9BC5B31CBE1C',
	'login': 'admin',
	'loginzh': 'undefined'
	}

respon = requests.post('http://10.252.0.15:8080/tmis/dllAction!datagrid.action', cookies=cookies)
print(respon.json())

a = respon.json()['rows']
for i in a:
	print(i['dll6'])