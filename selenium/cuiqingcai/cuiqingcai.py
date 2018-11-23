__author__='xjming'
#-*-coding:utf-08-*-
from mail import Email
from selenium import webdriver
import time

class CQC():
	def __init__(self):
		pass
	def get_title(self):
		self.browser = webdriver.Chrome()
		self.browser.get('https://cuiqingcai.com/category/technique/python')
		time.sleep(2)
		title = self.browser.find_element_by_xpath('/html/body/section/div[2]/div/article[1]/header/h2/a').text
		date = self.browser.find_element_by_xpath('/html/body/section/div[2]/div/article[1]/p/span[2]').text
		href = self.browser.find_element_by_xpath('/html/body/section/div[2]/div/article[1]/header/h2/a').get_attribute('href')
		self.browser.quit()
		return date,title,href

if __name__=='__main__':
	cqc = CQC()
	date,title,href = cqc.get_title()
	print(date,title,href)
	with open('cqc.txt','r') as f:
		old_title = f.read()
	if old_title!=title:
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','崔庆才博客文章')
		e.send("最新文章：%s\n时间：%s\n连接：%s"%(title,date,href))
		with open('cqc.txt','w') as f:
			f.write(title)