#! /use/bin/env python
#-*- coding:utf-8 -*-
from selenium import webdriver
from datetime import datetime

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')
input = browser.find_element_by_id('kw')
input.send_keys('火车票')
while True:
	now = datetime.now().strftime('%H:%M:%S')
	print(now)
	if now=='16:00:50':
		browser.find_element_by_id('su').click()
		break