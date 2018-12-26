# -*- coding: utf-8 -*-
import re,json
from action.excute_case import *
from action.get_case import *
from config.Config import *
from selenium import webdriver
from util.excel import *
from datetime import datetime
from util.mail import *
now = datetime.now()
file_list = os.listdir(case_path)
with open('report/report'+now.strftime('%Y-%m-%d')+'.txt','a') as f:
	f.write('Start Time:%s\n'%now.strftime('%Y-%m-%d %H:%M:%S'))
#加载测试用例
for file in file_list:
	if re.match(r'^test\_.*?\.xlsx',file):
		gc = GetCase(case_path+'\\'+file,'Sheet1')
		cases = gc.get_cases(gc.get_index())
		driver = webdriver.Chrome()
		result = excuteCase(driver,cases)
		driver.quit()
		with open('report/report'+now.strftime('%Y-%m-%d')+'.txt','a') as f:
			f.write('Test_suit:'+file.replace('.xlsx','')+'\n')
			f.write('Result:'+json.dumps(result)+'\n')
with open('report/report'+now.strftime('%Y-%m-%d')+'.txt','r') as f:
	results = re.findall(r'Start Time:(.*?)(?=Start Time|\Z)',f.read(),re.S)
	e = Email(SERVER,SENDER,PASSWORD,RECEIVER,CAPTION)
	e.send(results[-1])

