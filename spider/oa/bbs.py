from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time,requests,re
import mysql.connector

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'oa'
def insert_bbs(bbs_id,title,author,part):
	cnx = mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
	cur = cnx.cursor(buffered=True)
	sql = 'INSERT INTO bbs(bbs_id,title,author,part) VALUES (%(bbs_id)s,%(title)s,%(author)s,%(part)s)'
	value = {
		'bbs_id':bbs_id,
		'title':title,
		'author':author,
		'part':part
	}
	cur.execute(sql,value)
	cnx.commit()
	cur.close()
	cnx.close()

def insert_com(bbs_id,title,comment,author,part,time):
	cnx = mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
	cur = cnx.cursor(buffered=True)
	sql = 'INSERT INTO comment(bbs_id,title,comment,author,part,time) VALUES (%(bbs_id)s,%(title)s,%(comment)s,%(author)s,%(part)s,%(time)s)'
	value = {
		'bbs_id':bbs_id,
		'title':title,
		'comment':comment,
		'author':author,
		'part':part,
		'time':time
	}
	cur.execute(sql,value)
	cnx.commit()
	cur.close()
	cnx.close()

option = webdriver.ChromeOptions()
option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)
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
print(browser.get_cookies())
cookies = browser.get_cookies()
bbs_url = r"http://oa.grgbanking.com/interface2/portal2td.php?i=G0107805&t=1535508816&p=a0433892684808448&e=d4167f355496e52f70adc4ce7145f9ef&url=%2Fgeneral%2Fbbs"

s = requests.session()
c = requests.cookies.RequestsCookieJar()
for i in cookies:    #添加cookie到CookieJar
	c.set(i["name"], i["value"])
s.cookies.update(c)

res = s.get(bbs_url)
time.sleep(1)


bash_url = r"http://oa.grgbanking.com/general/bbs/board.php?BOARD_ID=32&PAGE_START="
for i in range(1,2541,20):
	url = bash_url+str(i)
	res = s.get(url)
	soup = BeautifulSoup(res.text,'lxml')
	article_list = soup.find_all('tr',class_='table_row')
	for article in article_list:
		try:
			link = article.find('a')['href']
			m = re.match('.*?COMMENT_ID=(.*?)\&.*?',link)
			bbs_id = m.group(1)
			title = article.find('a').get_text()
			author = article.find_all('td')[1].get_text()
			part = article.find_all('td')[2].get_text()
			print(title)
			insert_bbs(bbs_id,title,author,part)#保存标题	
			url = r"http://oa.grgbanking.com/general/bbs/"+link
			res = s.get(url)
			soup = BeautifulSoup(res.text,'lxml')
		except:
			print('保存标题失败')
			continue
		comments = soup.find_all('div',class_="comment_box")
		for comment in comments:
			try:
				info = comment.find('span',class_="info_span").get_text().replace(u'\xa0', u' ')
			#print(info.strip())
				m = re.match('作者姓名\：(.*?)\s部门\：(.*?)\s([\d\-\:\s]+)',info.strip())
				author = m.group(1)
				part = m.group(2)
				time = m.group(3)
				comment = comment.find(id=re.compile("content")).get_text()
				insert_com(bbs_id,title,comment,author,part,time)
			except:
				print('保存评论失败')
				continue