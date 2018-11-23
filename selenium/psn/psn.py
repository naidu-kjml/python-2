__author__='xjming'
#-*-coding:utf-08-*-
from mail import Email
from selenium import webdriver
import time

class PSN():
	def __init__(self):
		pass
	def get_mes(self):
		self.browser = webdriver.Chrome()
		self.browser.get('https://asia.playstation.com/cht-hk/ps4/')
		time.sleep(60)
		date = self.browser.find_element_by_xpath('//*[@id="_content_pscom_hk_zh_tw_ps4_jcr_content_par_section_1722301570_sectionParsys_layout_col1_layoutRowParsys_rss_list"]/ul/li[1]/a/span[1]').text
		mes = self.browser.find_element_by_xpath('//*[@id="_content_pscom_hk_zh_tw_ps4_jcr_content_par_section_1722301570_sectionParsys_layout_col1_layoutRowParsys_rss_list"]/ul/li[1]/a/span[2]').text
		self.browser.quit()
		return date,mes

if __name__=='__main__':
	psn = PSN()
	date,mes = psn.get_mes()
	print(date,mes)
	with open('psn.txt','r') as f:
		old_mes = f.read()
	if old_mes!=mes:
		e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','PSN更新')
		e.send("PSN有最新更新：\n时间：%s\n版本：%s"%(date,mes))
		with open('psn.txt','w') as f:
			f.write(mes)