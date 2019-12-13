__author__='xjming'
#-*-coding:utf-08-*-
from mail import Email
from selenium import webdriver
import time

class Deliver():
	def __init__(self,code,hour):
		self.code = code #运单号
		self.hour = hour #查询周期
	
	def open_broswer(self):
		option = webdriver.ChromeOptions()
		#option.add_argument('headless')
		option.add_argument('--log-level = 3')
		self.browser = webdriver.Chrome(options=option)
		self.browser.get('https://www.sogou.com/sgo?query=%E5%BF%AB%E9%80%92%E5%8D%95%E5%8F%B7%E6%9F%A5%E8%AF%A2&ie=utf8&_ast=1536807168&_asf=null&w=01029901&hdq=sogou-clse-7221e5c8ec6b08ef-0099&duppid=1&cid=&lxea=6-2-1-9.0.0.2502-3-CN4401-50-0-1-04E97A909FEB4B5C0B463D4193A27C61-42&s_from=result_up&sut=4958&sst0=1536807263968&lkt=0%2C0%2C0&sugsuv=003E59E77A0D4C925B99D1269F6A6614&sugtime=1536807263968')
		time.sleep(2)
		input = self.browser.find_element_by_xpath('//*[@id="sogou_vr_21194401_box_0"]/div[2]/div[1]/div[2]/input')
		input.clear()
		input.send_keys(self.code)
		time.sleep(2)
		self.browser.find_element_by_xpath('//*[@id="sogou_vr_21194401_button_0"]').click()

	def get_mes(self):
		self.browser.find_element_by_xpath('//*[@id="sogou_vr_21194401_button_0"]').click()
		time.sleep(2)
		t = self.browser.find_element_by_xpath('//*[@id="sogou_vr_21194401_box_0"]/div[2]/div[2]/div[1]/ul/li[1]/div[2]/div[1]').text
		mes = self.browser.find_element_by_xpath('//*[@id="sogou_vr_21194401_box_0"]/div[2]/div[2]/div[1]/ul/li[1]/div[2]/div[2]').text
		return t,mes
	
if __name__=='__main__':
	#code = input('请输入运单号：')
	code = "75318683541349"
	#t = input('请输入总共查询时间（小时）：')
	t = 20
	deliver = Deliver(code,t)
	init = '' #初始信息
	times = 1 #执行次数
	deliver.open_broswer()
	while True:
		print('第%d次查询'%times)
		times +=1
		if times>int(deliver.hour)*6:
			print('查询完成')
			break
		try:
			t,mes=deliver.get_mes()
			print("最新信息：\n时间：%s\n信息：%s"%(t,mes))
			if mes!=init and init!='':
				init = mes
				e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com',mes)
				e.send("最新快递：\n时间：%s\n信息：%s"%(t,mes))
		except:
			continue
		time.sleep(600)