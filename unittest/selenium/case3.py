# -*- coding: utf-8 -*-
import unittest,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class TestWork(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		#登录OA账号
		#logger.info('TEST START')
		#logger.info('OPEN BROWSER')
		cls.browser = webdriver.Chrome()
		cls.browser.maximize_window()
		#logger.info('CONNECTING TO "http://voa.grgbanking.com/"')
		cls.browser.get("http://voa.grgbanking.com/")
		#logger.info('SUCCESS')
		cls.browser.find_element_by_id('UserName').clear()
		cls.browser.find_element_by_id('UserName').send_keys('xjming9')
		cls.browser.find_element_by_id('UserKey').clear()
		cls.browser.find_element_by_id('UserKey').send_keys('grg7792042')
		cls.browser.find_element_by_class_name('login_list_btn').click()
		time.sleep(3)


	def test_work(self):
		#logger.info('test_work BEGIN')
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
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/b/span/input[2]').send_keys('06')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/input[3]').send_keys('软件测试')
			#第一项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[1]/textarea').send_keys('cas006硬币模块')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[2]/div/textarea').send_keys('第一周进行CAS002模块Linux版本测试。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[3]/textarea').send_keys('第一周完成CAS002模块测试，包括全部接口的功能和容错性。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[4]/td[5]/input').send_keys('25')
			#第二项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[1]/textarea').send_keys('TAM001')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[2]/textarea').send_keys('第二周进行TAM001模块Linux版本测试。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[3]/textarea').send_keys('第二周完成TAM001模块测试，测试全部接口功能和容错性。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[5]/td[5]/input').send_keys('25')
			#第三项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[1]/textarea').send_keys('MS80打印机')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[2]/textarea').send_keys('第三周进行MS80打印机测试。测试所有接口功能和容错性。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[3]/textarea').send_keys('第三周完成MS80打印机测试。')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[4]/input').send_keys('余雷')
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[6]/td[5]/input').send_keys('25')
			#第四项
			self.browser.find_element_by_xpath('//*[@id="body1"]/p[1]/span/font/font/table[3]/tbody/tr[7]/td[1]/textarea').send_keys('cas006硬币模块')
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
			self.assertEqual('2018年05月软件测试部肖佳明【运通智能】员工月度考核',con[:-9])
		except:
			self.browser.get_screenshot_as_file('./pic/test_genWork.png')
			#logger.error('test_genWork FAIL')
if __name__=='__main__':
	unittest.main()
