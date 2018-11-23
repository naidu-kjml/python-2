# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.log import logger

class TestLogin(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		logger.info('TEST START')
		logger.info('OPEN BROWSER')
		cls.browser = webdriver.Chrome()
		cls.browser.maximize_window()
		logger.info('CONNECTING TO "http://voa.grgbanking.com/"')
		cls.browser.get("http://voa.grgbanking.com/")
		logger.info('SUCCESS')
	
	@classmethod
	def tearDownClass(cls):
		#注销账号
		cls.browser.find_element_by_xpath('//*[@id="formMain"]/div[1]/div[1]/div/div/a').click()
		logger.info('TEST COMPLETE')
		time.sleep(3)
		cls.browser.quit()
	
	def test_login(self):
		logger.info('test_login BEGIN')
		try:
			user_name = 'xjming9'
			user_key = 'grg7792042'
			#输入账号
			self.browser.find_element_by_id('UserName').clear()
			self.browser.find_element_by_id('UserName').send_keys(user_name)
			#输入密码
			self.browser.find_element_by_id('UserKey').clear()
			self.browser.find_element_by_id('UserKey').send_keys(user_key)
			self.browser.find_element_by_class_name('login_list_btn').click()
			time.sleep(3)
			#断言
			self.assertEqual(self.browser.title,'广电运通门户')
			logger.info('test_login PASS')
		except:
			self.browser.get_screenshot_as_file('./pic/test_login.png')
