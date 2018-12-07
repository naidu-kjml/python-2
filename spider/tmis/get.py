# -*- coding: utf-8 -*-

__author__='xjming'
import time,re,requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

cookies = {
	'JSESSIONID':'F2C7E168255E8A2BD325D2069AFD46DC',
	'login':'admin',
	'dlxm':''
	}

respon = requests.post('http://10.1.34.82:8081/tmis/dllAction!datagrid.action',cookies=cookies)

a = respon.json()['rows']
oa_list = []
for i in a:
	oa_list.append(i['dll6'])

respon = requests.post('http://10.1.34.82:8081/tmis/softAction!datagrid.action',cookies=cookies)
a = respon.json()['rows']
for i in a:
	try:
		oa_list.append(i['oanumber'])
	except:
		continue

#登录OA账号

option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)
browser.get("http://voa.grgbanking.com/")
browser.find_element_by_id('UserName').clear()
browser.find_element_by_id('UserName').send_keys('lyjie9')
browser.find_element_by_id('UserKey').clear()
browser.find_element_by_id('UserKey').send_keys('jrjk2100')
browser.find_element_by_class_name('login_list_btn').click()
time.sleep(3)
browser.get('http://oa.grgbanking.com/vmobile/nav.php')

#切换到已办结页面
browser.switch_to.frame('main')
time.sleep(1)
browser.switch_to.frame('menu_top')
time.sleep(1)
browser.find_element_by_xpath('//*[@id="navMenu"]/a[6]/span').click()
time.sleep(3)
browser.switch_to.parent_frame()
browser.switch_to.frame('menu_main')
sum = 0
for i in range(0,10):
	#OA流程号
	oa = browser.find_element_by_xpath('//*[@id="%d"]/td[2]'%i).text
	if oa in oa_list:
		continue
	if browser.find_element_by_xpath('//*[@id="%d"]/td[3]/a'%i).text=="【运通智能】软件产品测试申请":
		browser.find_element_by_xpath('//*[@id="%d"]/td[4]/a'%i).click()
		time.sleep(3)	
		#切换页面句柄
		handle = browser.current_window_handle
		while True:
			time.sleep(1)
			handles = browser.window_handles
			if len(handles)==2:
				break
		for newhandle in handles:
			if newhandle!=handle:
				browser.switch_to_window(newhandle)
		time.sleep(1)
		browser.switch_to.frame('print_frm')
		#类别
		try:
			leibie = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[5]/td[3]/p').text.replace(u'\xa0', u' ')
			m = re.match(r'【测试机型】\s?(.*?)\s?(?=【工控机】)',leibie.strip())
			leibie = m.group(1).strip()
		except:
			leibie = ''
		#平台
		try:
			pingtai = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[6]/td[2]/p').text.replace(u'\xa0', u' ')
			m = re.match(r'【操作系统】\s?(.*?)\s?(?=【监控软件】)',pingtai.strip())
			pingtai = m.group(1).strip()
		except:
			pingtai = ''
		#模块
		mokuai = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[2]/td[2]/div').text
		#项目
		xiangmu = ''
		#版本号
		banbenhao = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[3]/td[4]/div/p').text
		#提交日期
		tjriqi = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/table/tbody/tr[11]/td[2]/span/span/span').text
		m = re.match(r'(.*?)(\d+\-\d+\-\d+)\s.*?',tjriqi.strip())
		tjriqi = m.group(2).strip()
		#提交人员
		tjry = m.group(1).strip()
		#状态
		try:
			if browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[1]/td[2]/p[2]'):
				zhuangtai = '测试完成'
		except:
			zhuangtai = "配置管理完成"
		#测试人员
		ceshirenyuan = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/div/div/table/tbody/tr[3]/td[4]').text
		#计划完成时间
		jhwcsj = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/div/div/table/tbody/tr[3]/td[3]').text
		#实际完成时间
		try:
			sjwcsj = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[2]/td[2]/span[2]/p/span[2]/span').text
			m = re.match(r'(.*?)(\d+\-\d+\-\d+)\s.*?',sjwcsj.strip())
			sjwcsj = m.group(2).strip()
		except:
			sjwcsj = ''
		#测试结果
		try:
			csjg = browser.find_element_by_xpath('//*[@id="bodyScroll"]/form/div[2]/div/div/div/div/table[2]/tbody/tr[2]/td[2]/span[2]/p/span[1]').text
		except:
			cejg = ''
		#判断测试类型为驱动还是整机
		list = ['张昕','周坤章']
		if tjry in list:
			postData = {
				"version":leibie,
				"dll1":pingtai,
				"dll2":mokuai,
				"dll3":'程序添加，需编辑',
				"dll4":banbenhao,
				"dll5":tjriqi,
				"dll6":oa,
				"dll7":zhuangtai,
				"dll8":ceshirenyuan,
				"dll9":jhwcsj,
				"dll10":sjwcsj,
				"dll11":csjg,
				"column20":'程序添加，需编辑'
				}

			cookies = {
				'JSESSIONID':'849271ABB41300EFFE03E1B0822CD06B',
				'login':'admin',
				'dlxm':''
				}

			try:
				respon = requests.post('http://10.1.34.82:8081/tmis/dllAction!add.action',data=postData,cookies=cookies)
				print('【%s】添加成功'%leibie)
				sum+=1
			except:
				print('【%s】添加失败！！！'%leibie)
		else:
			postData = {
			'diqu':'程序添加，需编辑',
			'xianlu':xiangmu,
			'sblx':mokuai,
			'bbh':banbenhao,
			'tjrq':tjriqi,
			'oanumber':oa,
			'status':zhuangtai,
			'tester':ceshirenyuan,
			'plantime':jhwcsj,
			'nowtime':sjwcsj,
			'testresult':csjg,
			'column20':'程序添加，需编辑'
			}
			cookies = {
				'JSESSIONID':'849271ABB41300EFFE03E1B0822CD06B',
				'login':'admin',
				'dlxm':''
				}
			try:
				respon = requests.post('http://10.1.34.82:8081/tmis/softAction!add.action',data=postData,cookies=cookies)
				print('【%s】添加成功'%mokuai)
				sum+=1
			except:
				print('【%s】添加失败！！！'%mokuai)
		browser.close()
		browser.switch_to_window(handle)
		browser.switch_to.frame('main')
		browser.switch_to.frame('menu_main')
browser.quit()
print('程序结束，完成添加%d条记录'%sum)
