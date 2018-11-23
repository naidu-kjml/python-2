import time,requests,os,re
test_url = 'https://www.baidu.com/'
timeout = 60
 
def test_proxy(proxy):
	try:
		proxies = {
			'http': proxy,
			'https':proxy.replace('http','https')
		}
		header = { 
		'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
		}

		start_time = time.time()
		requests.get(test_url, timeout=timeout, proxies=proxies,headers=header)
		end_time = time.time()
		used_time = end_time - start_time
		print('Proxy Valid', 'Used Time:', used_time)
		with open('validProxy.txt','a') as f:
			f.write(proxy)
		return True, used_time

if __name__=='__main__':
	with open('proxies.txt','r') as f:
		for proxy in f.readlines():
			print('testing %s'%proxy)
			test_proxy(proxy)
