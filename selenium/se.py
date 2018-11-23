#! //usr/bin/env python
#-*-coding:utf-8 -*-

from selenium import webdriver
browser = webdriver.Chrome()
browser.get("http://www.zhihu.com/explore")
print(browser.get_cookies())
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')