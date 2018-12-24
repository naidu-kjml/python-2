# -*- coding: utf-8 -*-
from config.Config import *
from action.get_case import *
from action.excute_case import *
from selenium import webdriver
from util.excel import *
import re

file_list = os.listdir(case_path)
for file in file_list:
	if re.match('^test\_.*?\.xlsx',file):
		gc = GetCase(case_path+'\\'+file,'Sheet1')
		cases = gc.get_cases(gc.get_index())
		driver = webdriver.Chrome()
		driver.maximize_window()
		excuteCase(driver,cases)
		driver.quit()