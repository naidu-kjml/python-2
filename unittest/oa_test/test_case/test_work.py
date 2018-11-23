# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from log import logger

class TestWork(unittest.TestCase):
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
		#删除已建工作，并注销账号。
		cls.browser.find_element_by_xpath('//*[@id="0"]/td[9]/a[1]').click()
		time.sleep(1)
		a = cls.browser.switch_to.alert
		a.accept()
		cls.browser.switch_to.parent_frame()
		cls.browser.switch_to.frame('menu_top')
		cls.browser.find_element_by_xpath('//*[@id="navMenu"]/a[4]/span').click()
		time.sleep(3)
		cls.browser.switch_to.parent_frame()		
		cls.browser.switch_to.frame('menu_main')
		time.sleep(1)
		d = cls.browser.find_element_by_xpath('//*[@id="act_0"]/span')
		ActionChains(cls.browser).move_to_element(d).perform()
		time.sleep(1)
		cls.browser.find_element_by_xpath('//*[@id="act_0_menu"]/a[5]').click()
		time.sleep(1)
		a = cls.browser.switch_to.alert
		a.accept()
		cls.browser.quit()
	
	def test_work(self):
		logger.info('test_work BEGIN')
		try:
			self.browser.find_element_by_xpath("//div[@id = 'MenuID']/ul/li[4]").click()
			self.browser.find_element_by_xpath("//div[@id = 'MenuID']/ul/li[4]/ul/li").click()
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
			self.browser.find_element_by_xpath('//div[@id="xtree1"]/ul/li[13]/span/a').click()
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="xtree1"]/ul/li[13]/ul/li[3]/span/a').click()
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="xtree1"]/ul/li[13]/ul/li[3]/ul/li[4]/span/a').click()
			time.sleep(1)
			self.browser.switch_to.frame('page')
			time.sleep(1)
			self.browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[3]/td/input[4]').click()
			time.sleep(1)
			#切换回主页面
			self.browser.switch_to.default_content()
			time.sleep(1)
			#切换至frame
			self.browser.switch_to.frame('workflow-form-frame')
			time.sleep(1)

			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/b/span/input[1]').send_keys('2018')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/b/span/input[2]').send_keys('08')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/input[3]').send_keys('软件测试')
			#第一项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[1]/textarea').send_keys('BIM2020')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[2]/div/textarea').send_keys('第一周进行BIM2020模块测试,验证是否禁用第四版人民币，以及其他接口基本功能测试。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[3]/textarea').send_keys('第一周完成BIM2020模块测试，并提交测试报告。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[5]/input').send_keys('25')
			#第二项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[1]/textarea').send_keys('BA08')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[2]/textarea').send_keys('第二周进行BA08模块V1.0.1b43版本测试，验证多个版本已修改的功能。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[3]/textarea').send_keys('第二周完成BA08模块测试，并提交测试报告。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[5]/input').send_keys('25')
			#第三项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[1]/textarea').send_keys('MRTD证件机读模块')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[2]/textarea').send_keys('第三周进行MRTD证件机读模块测试。验证上一版本修复的问题')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[3]/textarea').send_keys('第三周完成MRTD证件机读模块测试，并提交测试报告。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[5]/input').send_keys('25')
			#第四项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[1]/textarea').send_keys('BR15N模块')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[2]/textarea').send_keys('第四周进行BR15N模块Linux版本测试。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[3]/textarea').send_keys('第四周完成BR15N模块Linux版本测试，测试所有接口功能和容错性。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[5]/input').send_keys('25')
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="form_control"]/table/tbody/tr/td[2]/input[1]').click()
			time.sleep(3)
			self.browser.find_element_by_xpath('//*[@id="SMS_REMIND_NEXT"]').click()
			self.browser.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[5]/td[1]/input[13]').click()
			time.sleep(1)
			self.browser.switch_to.default_content()
			time.sleep(1)
		#切换至frame
			self.browser.switch_to.frame('main')
			time.sleep(1)
			self.browser.switch_to.frame('menu_top')
			time.sleep(1)
			self.browser.find_element_by_xpath('//*[@id="navMenu"]/a[6]/span').click()
			time.sleep(3)
			self.browser.switch_to.parent_frame()
			self.browser.switch_to.frame('menu_main')
			con = self.browser.find_element_by_xpath('//*[@id="0"]/td[4]/a').text
			print(con[:-9])
			#断言：对比内容是否相同
			self.assertEqual('2018年08月软件测试部肖佳明【运通智能】员工月度考核',con[:-9])
		except:
			self.browser.get_screenshot_as_file('./pic/test_genWork.png')
			logger.error('test_genWork FAIL')
