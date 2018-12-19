import time,requests,os,re
from bs4 import BeautifulSoup

headers = {
	"User_Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Referer" : "http://www.baidu.com"
}



test_url = 'https://www.baidu.com/'
timeout = 60
 
def test_proxy(proxy):
	proxies = {
		'https': proxy
	#	'https':proxy.replace('http','https')
	}

	start_time = time.time()
	res = requests.get(test_url,timeout=timeout,proxies=proxies,headers=headers)
	print(res.status_code)
	print(res.text)
	end_time = time.time()
	used_time = end_time - start_time
	print('Proxy Valid', 'Used Time:', used_time)
	if res.status_code==200:
		with open('validProxy.txt','a') as f:
			f.write(proxy+'\n')
			time.sleep(3)


if __name__=='__main__':
	bash_url = 'http://www.89ip.cn/index_'
	proxy = []
	for i in range(1,100):
		url = bash_url+str(i)+'.html'
		response = requests.get(url,headers=headers)
		response.encoding = 'utf-8'
		soup = BeautifulSoup(response.text,'lxml')
		proxies = soup.find('table',class_='layui-table').find('tbody').find_all('tr')
		for proxie in proxies:
			ip = proxie.find_all('td')[0].text
			port = proxie.find_all('td')[1].text
			pro = 'https://'+ip.strip()+':'+port.strip()
			try:
				test_proxy(pro)
			except:
				continue
		

