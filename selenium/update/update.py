from selenium import webdriver
import time

url = 'https://image.baidu.com/'

browser = webdriver.Chrome()
browser.get(url)
time.sleep(3)
browser.find_element_by_xpath('//*[@id="sttb"]').click()
time.sleep(1)
browser.find_element_by_xpath('//*[@id="stfile"]').send_keys(r'D:\errcode\images\background.jpg')
time.sleep(5)

