#-*-coding:utf-8 -*-
import os,requests
from bs4 import BeautifulSoup

headers = {
	"User_Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Referer" : "http://www.baidu.com"
}

bash_url = 'http://www.89ip.cn/index_'
for i in range(1,100):
	url = bash_url+str(i)+'.html'
	response = requests.get(url,headers=headers)
	response.encoding = 'utf-8'
	soup = BeautifulSoup(response.text,'lxml')
	proxies = soup.find('table',class_='layui-table').find('tbody').find_all('tr')
	for proxie in proxies:
		ip = proxie.find_all('td')[0].text
		port = proxie.find_all('td')[1].text
		pro = 'http://'+ip.strip()+':'+port.strip()+'\n'
		with open('proxies.txt','a') as f:
			f.write(pro)