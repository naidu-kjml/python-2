# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from utils.log import logger

class TestDiary(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		#登录OA账号
		logger.info('TEST START')
		logger.info('OPEN BROWSER')
		cls.browser = webdriver.Chrome()
		cls.browser.maximize_window()
		logger.info('CONNECTING TO "http://voa.grgbanking.com/"')
		cls.browser.get("http://voa.grgbanking.com/")
		logger.info('SUCCESS')
		cls.browser.find_element_by_id('UserName').clear()
		cls.browser.find_element_by_id('UserName').send_keys('xjming9')
		cls.browser.find_element_by_id('UserKey').clear()
		cls.browser.find_element_by_id('UserKey').send_keys('grg7792042')
		cls.browser.find_element_by_class_name('login_list_btn').click()
		time.sleep(3)

	@classmethod
	def tearDownClass(cls):
		#删除日志
		cls.browser.find_element_by_xpath('/html/body/div[2]/table[1]/tbody/tr/td[2]/input').click()
		cls.browser.find_element_by_xpath('/html/body/div[2]/div[11]/input[2]').click()
		time.sleep(1)
		a = cls.browser.switch_to.alert
		a.accept()
		time.sleep(2)
		cls.browser.quit()
	def test_diary(self):
		logger.info('test_diary BEGIN')
		try:
			self.browser.find_element_by_xpath('//*[@id="MenuID"]/ul/li[1]/a').click()
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="MenuID"]/ul/li[1]/ul/li[10]/a').click()
			#切换页面句柄
			handle = self.browser.current_window_handle
			while True:
				time.sleep(1)
				handles = self.browser.window_handles
				if len(handles)==2:
					break
			for newhandle in handles:
				if newhandle!=handle:
					self.browser.switch_to_window(newhandle)
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="Toolbar"]/a[2]/span').click()
			time.sleep(1)
			self.browser.switch_to.frame('diary_body')
			time.sleep(3)
			self.browser.switch_to.frame(self.browser.find_element_by_xpath('//*[@id="cke_contents_CONTENT"]/iframe'))
			con1 = '''1.测试BR15模块。 8h
发现问题：
1、设置串口成功，但是返回失败。
2、历史修改记录文档版本号错误，应为V2.0.2b27
3、获取钞票信息接口，钞票面向参数错误。
4、循环鼓满时，接收钞票去向显示为暂存。'''
			self.browser.find_element_by_xpath('/html').send_keys(con1)
			time.sleep(1)
			self.browser.switch_to.default_content()
			self.browser.switch_to.frame('diary_body')
			self.browser.find_element_by_xpath('//*[@id="diary_change"]/td/div').click()
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="SMS_REMIND"]').click()
			self.browser.find_element_by_xpath('/html/body/form/table/tbody/tr[9]/td/input[3]').click()
			time.sleep(3)
			#获取第一条日志内容
			con2 = self.browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]').text
			print(con2)
			time.sleep(3)
			#断言：对比内容是否相同
			self.assertMultiLineEqual(con1,con2)
		except:
			self.browser.get_screenshot_as_file('./pic/test_diary.png')
			logger.error('test_diary FAIL')
