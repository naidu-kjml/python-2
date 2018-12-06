# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



#登录OA账号

#option = webdriver.ChromeOptions()
#option.add_argument('headless')
#browser = webdriver.Chrome(chrome_options=option)
browser = webdriver.Chrome()
browser.get("http://voa.grgbanking.com/")
browser.find_element_by_id('UserName').clear()
browser.find_element_by_id('UserName').send_keys('xjming9')
browser.find_element_by_id('UserKey').clear()
browser.find_element_by_id('UserKey').send_keys('grg7792042')
browser.find_element_by_class_name('login_list_btn').click()
time.sleep(3)
browser.get('http://oa.grgbanking.com/vmobile/nav.php')

#切换到已办结页面
browser.switch_to.frame('main')
time.sleep(1)
browser.switch_to.frame('menu_top')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="navMenu"]/a[6]/span').click()
time.sleep(3)
browser.switch_to.parent_frame()
browser.switch_to.frame('menu_main')
print (browser.current_url)
for i in range(0,1):
	if browser.find_element_by_xpath('//*[@id="%d"]/td[3]/a'%i).text=="【运通智能】软件产品测试申请":
		browser.find_element_by_xpath('//*[@id="%d"]/td[4]/a'%i).click()
		time.sleep(3)	
		print (browser.current_url)
		#切换页面句柄
		handle = browser.current_window_handle
		while True:
			time.sleep(1)
			handles = browser.window_handles
			if len(handles)==2:
				break
		for newhandle in handles:
			if newhandle!=handle:
				browser.switch_to_window(newhandle)
		time.sleep(3)
		browser.switch_to.frame('print_frm')
		print (browser.current_url)
		print(browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[2]/td[2]/div').text)

