from selenium import webdriver
import json,time

def excuteCase(driver,cases):
	driver.implicitly_wait(3)#隐式等待
#	with open("test.json", "w", encoding='utf-8') as f:
#		f.write(json.dumps(a, indent=4))
	for case in cases:#遍历用例
		print('testing case:'+case)
		for step in cases[case]:#遍历步骤
			print('STEP:'+step)
			#遍历步骤内容
			url = cases[case][step]['url']
			control_id = cases[case][step]['control_id']
			control_action = cases[case][step]['control_action'] 
			data = cases[case][step]['data'] 
			expectation = cases[case][step]['expectation'] 
			option = cases[case][step]['option'] 
			#print(url,control_id,control_action,data,expectation,option)
			if url != None:
				driver.get(url)
			else:
				if control_action == 'click':#点击操作
					if option == 'xpath' or option == 'alert':
						driver.find_element_by_xpath(control_id).click()
					elif option == 'id':
						driver.find_element_by_id(control_id).click()
					elif option == 'name':
						driver.find_element_by_name(control_id).click()
					elif option == 'class':
						driver.find_element_by_class_name(control_id).click()
				else:#输入操作
					if option == 'xpath' or option == 'alert':
						driver.find_element_by_xpath(control_id).clear()
						driver.find_element_by_xpath(control_id).send_keys(data)
					elif option == 'id':
						driver.find_element_by_id(control_id).clear()
						driver.find_element_by_id(control_id).send_keys(data)
					elif option == 'name':
						driver.find_element_by_name(control_id).clear()
						driver.find_element_by_name(control_id).send_keys(data)
					elif option == 'class':
						driver.find_element_by_class_name(control_id).clear()
						driver.find_element_by_class_name(control_id).send_keys(data)
				time.sleep(3)
				try:
					if expectation != None:#断言
						if option == 'xpath':
							driver.find_element_by_xpath(control_id)
						elif option == 'alert':
							if driver.switch_to_alert().text == expectation:
								pass
								driver.switch_to_alert().accept()
						elif option == 'id':
							driver.find_element_by_id(control_id)
						elif option == 'name':
							driver.find_element_by_name(control_id)
						elif option == 'class':
							driver.find_element_by_class_name(control_id)
				except:
					print(case+' False!!!')
					break
		print(case+" Pass!!!")




if __name__=='__main__':
	driver = webdriver.Chrome()
	excuteCase(driver)
	driver.quit()