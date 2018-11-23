#! /usr/bin/env pyhton
#-*-coding:utf-8 -*-

import requests,re,time,smtplib
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header

times = 1
url = 'http://yijiaren201703.cn/index.php?s=/addon/yijiaren/mobile/search_ticket/mpid/2/from/%E3%80%90%E6%B8%85%E6%98%8E%E5%8C%85%E8%BD%A6%E3%80%91%E5%B9%BF%E5%B7%9E%E5%88%B0%E8%95%89%E5%B2%AD+%E6%A2%85%E5%8E%BF%EF%BC%88140%E5%85%83%EF%BC%89/to/%E8%95%89%E5%9F%8E+%E6%96%87%E5%B9%BF%E7%A6%8F+%E6%A2%85%E5%8E%BF/datetime/2018-04-04'
r = requests.get(url)

print(r.status_code)
a=BeautifulSoup(r.text,'lxml').find('p',class_='info').get_text()
ticket_num = str(re.search('成人票余:(.*?)张',a)[1])
while True:
	print(datetime.now())
	print('第%d次获取余票'%times)
	a=BeautifulSoup(r.text,'lxml').find('p',class_='info').get_text()
	ticket_num = int(re.search('成人票余:(.*?)张',a)[1])
	print('当前车票剩余：%d张'%ticket_num)
	if ticket_num<3:
		user = '15989104405@163.com'
		pwd = 'wy7792042'
		to = ['13250790293@163.com']
		msg = MIMEMultipart()
		msg['Subject'] = Header('包车', 'utf-8')
		msg['From'] = Header(user)

		content1 = MIMEText('车票数量低！！！！', 'plain', 'utf-8')
		msg.attach(content1)

		s = smtplib.SMTP('smtp.163.com')
		s.set_debuglevel(1)              #调试使用
		s.starttls()                     #建议使用
		s.login(user, pwd)
		s.sendmail(user, to, msg.as_string())
		s.close()
		break
	times = times+1
	time.sleep(60)
