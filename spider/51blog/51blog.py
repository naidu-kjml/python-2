# -*- coding: utf-8 -*-

import requests, re, csv
from bs4 import BeautifulSoup

base_url = 'https://blog.51cto.com/xqtesting'

for i in range(1,41):
	url = base_url+'/p'+str(i)
	print(url)
	respons = requests.get(url)
	soup = BeautifulSoup(respons.text, 'lxml')
	items = soup.find('ul', class_='artical-list').find_all('li')
	for item in items:
		title = item.find('a', class_='tit').get_text().replace('置顶', '').strip()
		link = item.find('a', class_='tit')['href']
		time = re.match(r'发布于：(.*)',item.find('a', class_='time fl').get_text()).group(1)
		try:
			read = item.find('div', class_='bot').find('p', class_='read fl').get_text().replace(u'\xa0', u' ').replace('阅读', '')
		except:
			read = item.find('div', class_='bot').find('p', class_='read fl on').get_text().replace(u'\xa0', u' ').replace('阅读', '')
		l = [time, title, link, read]
		with open('51blog.csv','a',newline='')as f:
			writer = csv.writer(f)
			writer.writerow(l)