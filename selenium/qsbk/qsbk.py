#! /usr/bin/env python
# -*- coding:utf-8 -*-
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
browser.get('https://www.qiushibaike.com/text/')
response = browser.page_source
divs = BeautifulSoup(response,'lxml').find_all('div',{"class":re.compile('article block untagged mb15.*?')})
for div in divs:
    print(div)

