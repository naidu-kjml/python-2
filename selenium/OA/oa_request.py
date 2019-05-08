import requests
#import time,mysql.connector

MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_PORT = '3306'
MYSQL_DB = 'oa'
UserID = 'G0107805'
USER_ID = 'xjming9'
USER_NAME = '肖佳明'


def insert_oa(EMPLOYEE_NAME,EMPLOYEE_NO,GENDER,IN_DATE,ATTRIBUTE6,OEMAIL,MOBILE_NO,POSITION_NAME,DEPT_FULL_NAME):
	cnx = mysql.connector.connect(user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOSTS,database=MYSQL_DB)
	cur = cnx.cursor(buffered=True)
	sql = 'INSERT INTO oa(EMPLOYEE_NAME,EMPLOYEE_NO,GENDER,IN_DATE,ATTRIBUTE6,OEMAIL,MOBILE_NO,POSITION_NAME,DEPT_FULL_NAME) VALUES (%(EMPLOYEE_NAME)s,%(EMPLOYEE_NO)s,%(GENDER)s,%(IN_DATE)s,%(ATTRIBUTE6)s,%(OEMAIL)s,%(MOBILE_NO)s,%(POSITION_NAME)s,%(DEPT_FULL_NAME)s)'
	value = {
		'EMPLOYEE_NAME':EMPLOYEE_NAME,
		'EMPLOYEE_NO':EMPLOYEE_NO,
		'GENDER':GENDER,
		'IN_DATE':IN_DATE,
		'ATTRIBUTE6':ATTRIBUTE6,
		'OEMAIL':OEMAIL,
		'MOBILE_NO':MOBILE_NO,
		'POSITION_NAME':POSITION_NAME,
		'DEPT_FULL_NAME':DEPT_FULL_NAME
	}
	cur.execute(sql,value)
	cnx.commit()
	cur.close()
	cnx.close()
	
def login():
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
	s = requests.session()
	bash_url = 'http://voa.grgbanking.com/'
	response = s.get(bash_url, headers=headers)
	'''soup = BeautifulSoup(response.text,'lxml')
	pubkey = soup.find('input',id='tra')['value'] 
	#key = urllib.parse.quote(rsa_encrypt('grg7792042', pubkey)).replace('+', '%2B')
	key = rsa_encrypt('grg7792042', pubkey)
	#print(key)
	url = 'http://voa.grgbanking.com/HandlerGRGPortal.ashx'
	payload = {
		'method': 'getLoginTD',
		'UserName': 'xjming9',
		'UserKey': key,
		'ValidateCode': '',
		'NErrorCount': 0
	}
	response = s.post(url, data=payload)
	#print(response.json())
	url = response.json()['data']
	resultData = s.get(url).json()['resultData']'''
	#只需工号和姓名即可登录
	payload = {
	'method': 'GoToIndex',
	'USER_ID': USER_ID,
	'EMPID': UserID,
	'USER_NAME': USER_NAME
	}
	url = 'http://voa.grgbanking.com/HandlerGoToIndex.ashx'
	response = s.post(url, data=payload, headers=headers)
	url = 'http://voa.grgbanking.com/Index.aspx'
	response = s.get(url, headers=headers)
	return s
	
def getDeptAsyncTree(s,id,name):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
	data = {
		'id': id,
		'name': name,
		'deptoruser': '',
		'otherParam': 'zTreeAsyncTest'
	}
	url = 'http://voa.grgbanking.com/HandlerAddressList.ashx?method=getDeptAsyncTree'
	response = s.post(url, data=data, headers=headers)
	list = response.json()['rows']
	for i in list:
		if i['beiyong'] != None:
			HandlerAddressList(s,i['id'],i['beiyong'])
		else:
			getDeptAsyncTree(s,i['id'],i['name'])

def HandlerAddressList(s,UserID,POSITION_ID):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
	data = {
		'method': 'getUser',
		'UserID': UserID,
		'POSITION_ID': POSITION_ID
	}
	url = 'http://voa.grgbanking.com/HandlerAddressList.ashx'
	response = s.post(url, data=data, headers=headers)
	print(response.json()['data']['EMPLOYEE_NAME'])
	
	
if __name__=='__main__':
	s = login()
	getDeptAsyncTree(s,2471,'运通智能')
		