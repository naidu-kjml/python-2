#! usr/bin/env python 
#-*- coding:utf-8 -*-

import os,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

with open('errcode.txt','r') as f:
	errcodes = f.read()

browser = webdriver.Chrome()
browser.get("http://www.errcode.tk")
input = browser.find_element_by_id('ErrCode')
button = browser.find_element_by_class_name('btn')
locator = ('id','ec')
input.send_keys('14410')
button.click()
t = 0 #总共花费时间
sum = 0 #查询次数
for e in errcodes.split('\n'):
	input.clear()
	input.send_keys(e)
	start = time.time()
	button.click()
	try:
		element = WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element(locator,e))
		end = time.time()
		costtime = end-start
		t += costtime
		sum +=1
		print('%s use time:%s'%(browser.find_element_by_id('ec').text,costtime))
		with open('costtime.txt','a') as f:
			f.write(str(costtime)+'\n')
		time.sleep(3)
	except:
		print('errcode not exist')
print('totle time:%s'%str(t))
print('ave time:%s'%str(t/sum))
browser.close()
	