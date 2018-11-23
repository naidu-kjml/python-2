from selenium import webdriver
import time,mysql.connector

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'oa'
def insert_oa(name,id,part,position,phone,date):
	cnx = mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
	cur = cnx.cursor(buffered=True)
	sql = 'INSERT INTO oa(name,id,part,position,phone,date) VALUES (%(name)s,%(id)s,%(part)s,%(position)s,%(phone)s,%(date)s)'
	value = {
		'name':name,
		'id':id,
		'part':part,
		'position':position,
		'phone':phone,
		'date':date
	}
	cur.execute(sql,value)
	cnx.commit()
	cur.close()
	cnx.close()

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

time.sleep(2)
browser.find_element_by_xpath('//*[@id="formMain"]/div[1]/div[1]/div/ul/li[5]/a').click()
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
		
#点击运通智能
browser.find_element_by_xpath('//*[@id="GRG_OrganizationalStructureTree_13_switch"]').click()
for i in range(15,30):
	browser.find_element_by_xpath('//*[@id="GRG_OrganizationalStructureTree_%i_switch"]'%i).click()
	time.sleep(0.5)
time.sleep(1)
for i in range(140,143):
	browser.find_element_by_xpath('//*[@id="GRG_OrganizationalStructureTree_%i_switch"]'%i).click()
	time.sleep(0.5)
time.sleep(1)
for i in range(201,208):
	browser.find_element_by_xpath('//*[@id="GRG_OrganizationalStructureTree_%i_switch"]'%i).click()
	time.sleep(1)
time.sleep(1)
for i in range(30,305):
	browser.find_element_by_xpath('//*[@id="GRG_OrganizationalStructureTree_%i_span"]'%i).click()
	time.sleep(0.3)
	print(browser.find_element_by_xpath('//*[@id="span3"]').text)
	name = browser.find_element_by_xpath('//*[@id="span3"]').text
	phone = browser.find_element_by_xpath('//*[@id="span10"]').text
	id = browser.find_element_by_xpath('//*[@id="span1"]').text
	position = browser.find_element_by_xpath('//*[@id="span5"]').text
	part = browser.find_element_by_xpath('//*[@id="span13"]').text
	date = browser.find_element_by_xpath('//*[@id="span6"]').text
	insert_oa(name,id,part,position,phone,date)






