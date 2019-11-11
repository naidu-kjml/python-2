__author__='xjming'
#-*-coding:utf-08-*-
from mail import Email
import time, requests, re
from bs4 import BeautifulSoup

class PSN():
	def __init__(self):
		pass
	def get_mes(self):
		response = requests.get('https://asia.playstation.com/cht-hk/ps4/system-update/')
		soup = BeautifulSoup(response.text, 'lxml')
		mes = soup.find('h2', class_='js-style lg-center xs-font28').text.strip()
		date = soup.find_all('div', class_='parsys sectionParsys')[1].find('div', class_='baseComponent section text').text.strip()
		m = re.match(r'自(.*?)起.*?',date)
		date = m.group(1).strip()
		return mes,date

if __name__=='__main__':
	psn = PSN()
	try:
		mes,date = psn.get_mes()
		with open('psn.txt','r') as f:
			old_mes = f.read()
		if old_mes!=mes:
			print('有更新')
			print(date,mes)
			e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','PSN更新')
			e.send("PSN有最新更新：\n时间：%s\n版本：%s"%(date,mes))
			with open('psn.txt','w') as f:
				f.write(mes)
		print('无需更新')
		print(mes,date)
	except:
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','PSN更新')
		e.send("脚本异常")		