from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
driver.find_element_by_id('kw').send_keys('selenium')
driver.find_element_by_id('su').click()
time.sleep(3)

js = "var q=document.documentElement.scrollTop=10000"
driver.execute_script(js)
time.sleep(3)