import unittest,time
from ec import *
from selenium import webdriver


class TestEc(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print('启动Chrome')
		cls.browser = webdriver.Chrome()
		cls.browser.maximize_window()
		cls.browser.get("http://www.errcode.tk")
		print('启动成功，测试开始*********')
	
	@classmethod
	def tearDownClass(cls):
		print('测试结束！！！！！！！！')
		cls.browser.quit()
	
	def test_search(self):
		e = '144'
		self.assertEqual(e,search(self.browser,e))
		
	def test_noexist(self):
		e = '0000'
		self.assertEqual('错误码不存在',no_exist(self.browser,e))
		
	def test_ale(self):
		ale(self.browser)
		a = self.browser.switch_to.alert
		self.assertEqual('请输入错误码',a.text)
		a.accept()