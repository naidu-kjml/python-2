__author__='xjming'
#-*-coding:utf-08-*-
from mail import Email
import time, requests
from bs4 import BeautifulSoup

class PSN():
	def __init__(self):
		pass
	def get_mes(self):
		response = requests.get('https://asia.playstation.com/cht-hk/ps4/')
		soup = BeautifulSoup(response.text, 'lxml')
		mes = soup.find('li', class_='psc-pdt16 psc-pdb16 psc-bb-dot').find('span', class_='psc-d-block psc-of-hidden').text
		date = soup.find('li', class_='psc-pdt16 psc-pdb16 psc-bb-dot').find('span', class_='psc-info-date').text.strip()
		return date,mes

if __name__=='__main__':
	psn = PSN()
	date,mes = psn.get_mes()
	with open('psn.txt','r') as f:
		old_mes = f.read()
	if old_mes!=mes:
		print('有更新')
		print(date,mes)
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','PSN更新')
		e.send("PSN有最新更新：\n时间：%s\n版本：%s"%(date,mes))
		with open('psn.txt','w') as f:
			f.write(mes)
	print(date,mes)