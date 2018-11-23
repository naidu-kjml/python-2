# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.log import logger

class TestEc(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		logger.info('TEST_SEARCH START')
		logger.info('OPEN BROWSER')
		cls.browser = webdriver.Chrome()
		cls.browser.maximize_window()
		logger.info('CONNECTING TO "http://www.errcode.tk"')
		cls.browser.get("http://www.errcode.tk")
		logger.info('SUCCESS')
	
	@classmethod
	def tearDownClass(cls):
		logger.info('TEST_SEARCH COMPLETE')
		cls.browser.quit()
	
	def test_01search(self):
		logger.info('TEST_CASE1 BEGIN')
		try:
			e = '14410'
			locator = ('id','ec')
			self.browser.find_element_by_id('ErrCode').clear()
			self.browser.find_element_by_id('ErrCode').send_keys(e)
			self.browser.find_element_by_class_name('btn').click()
			element = WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element(locator,e))
			result = self.browser.find_element_by_id('ec').text
			self.assertEqual(e,result)
			logger.info('TEST_CASE1 PASS')

		except:
			self.browser.get_screenshot_as_file('./pic/test_case1.png')
			logger.error('TSET_CASE1 FAIL')
		
'''	def test_02noExist(self):
		logger.info('TEST_CASE2 BEGIN')
		self.browser.refresh()#刷新页面
		e = '0000'
		locator = ('id','err')
		self.browser.find_element_by_id('ErrCode').clear()
		self.browser.find_element_by_id('ErrCode').send_keys(e)
		self.browser.find_element_by_class_name('btn').click()
		element = WebDriverWait(self.browser, 10).until(EC.text_to_be_present_in_element(locator,'错误码不存在'))
		result = self.browser.find_element_by_id('err').text
		self.assertEqual('错误码不存在',result)
		logger.info('TEST_CASE2 PASS')
	def test_03alert(self):
		logger.info('TEST_CASE3 BEGIN')
		self.browser.refresh()#刷新页面
		self.browser.find_element_by_id('ErrCode').clear()
		self.browser.find_element_by_class_name('btn').click()
		time.sleep(1)
		a = self.browser.switch_to.alert
		self.assertEqual('请输入错误码',a.text)
		a.accept()
		logger.info('TEST_CASE3 PASS')'''