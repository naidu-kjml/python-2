#! usr/bin/env python 
#-*- coding:utf-8 -*-

import os,time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait





def search(browser,e):
	locator = ('id','ec')
	browser.find_element_by_id('ErrCode').clear()
	browser.find_element_by_id('ErrCode').send_keys(e)
	browser.find_element_by_class_name('btn').click()
	element = WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element(locator,e))
	return browser.find_element_by_id('ec').text
	
def no_exist(browser,e):
	locator = ('id','err')
	browser.find_element_by_id('ErrCode').clear()
	browser.find_element_by_id('ErrCode').send_keys(e)
	browser.find_element_by_class_name('btn').click()
	element = WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element(locator,'错误码不存在'))
	return browser.find_element_by_id('err').text
	
def ale(browser):
	browser.find_element_by_id('ErrCode').clear()
	browser.find_element_by_class_name('btn').click()
	time.sleep(1)