import unittest,time
from selenium import webdriver

#1、打开Chrome浏览器
browser = webdriver.Chrome()
browser.maximize_window()
#2、访问登录页面
browser.get("http://voa.grgbanking.com/Login.aspx")
#3、输入用户名
browser.find_element_by_id('UserName').clear()
browser.find_element_by_id('UserName').send_keys('xjming9')
#4、输入密码
browser.find_element_by_id('UserKey').clear()
browser.find_element_by_id('UserKey').send_keys('grg7792042')
#5、点击登录按钮
browser.find_element_by_class_name('login_list_btn').click()
#6、注销账号、关闭浏览器
browser.find_element_by_xpath('//*[@id="formMain"]/div[1]/div[1]/div/div/a').click()
browser.quit()