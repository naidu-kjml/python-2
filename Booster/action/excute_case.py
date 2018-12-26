from selenium import webdriver
import json,time
from action.autoDriver import *
from util.log import logger
from config.Config import *

def excuteCase(driver,cases):
	ad = AutomateDriver(driver)
	ad.driver.implicitly_wait(3)#隐式等待
	case_index = 0#初始化用例号为0
	Test_case = {}
	for case in cases:#遍历用例
		try:
			case_index += 1
			step_index = 0#初始化用例步骤号为0
			print('Testing %dth case:%s'%(case_index,case))
			logger.info('Testing %dth case:%s'%(case_index,case))
			for step in cases[case]:#遍历步骤
				step_index += 1
				print('STEP%d:%s'%(step_index,step))
				logger.info('STEP%d:%s'%(step_index,step))
				#获取步骤内容
				url = cases[case][step]['url']
				control_id = cases[case][step]['control_id']
				control_action = cases[case][step]['control_action'] 
				data = cases[case][step]['data'] 
				expectation = cases[case][step]['expectation'] 
				option = cases[case][step]['option']
				selector = str(option)+','+str(control_id)
				#执行用例
				if control_action == 'get':
					ad.navigate(url)
				elif control_action == 'post':
					pass
				elif control_action == 'click':
					ad.click(selector)
				elif control_action == 'send_keys':
					ad.type(selector,data)
				elif control_action == 'openNewWindow':
					ad.openNewWindow(selector)
				#断言
				if expectation == None:
					continue
				selector = str(option)+','+str(expectation)
				ad.getElement(selector)
				if option == 'alert':
					rel = ad.getAlertText()
					if rel == expectation:
						ad.acceptAlert()
					else:
						raise BaseException
		except:
			Test_case[case] = 'Fail'
			print(case+' Fail!!!')
			logger.error(case+' Fail!!!')
			ad.get_screenshot(screenshot_path+case+'.png')
			continue
		else:
			Test_case[case] = 'Pass'
			print(case+" Pass!!!")
			logger.info(case+' Pass!!!')
	return Test_case



'''if __name__=='__main__':
	driver = webdriver.Chrome()
	excuteCase(driver，cases)
	driver.quit()'''