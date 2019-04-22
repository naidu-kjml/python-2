# coding=utf-8
import base64, requests, re
import rsa, urllib, time, json
from bs4 import BeautifulSoup


UserID = 'G0108228'
USER_ID = 'lyjie9'
USER_NAME = '赖雅洁'

__all__ = ['rsa_encrypt']


def _str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    if len(b_str) < 162:
        return False

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]

    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    '''
    rsa加密
    :param s:
    :param pubkey_str:公钥
    :return:
    '''
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()

 
def login(s):
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
	#  获取首页的待办工作
	'''soup = BeautifulSoup(response.text, 'lxml')
	CheckString = soup.find('input', id='CheckString')['value']
	#print(CheckString)
	sFlowURL = 'http://oa.grgbanking.com'+"/interface2/workflow_list2.php?"+CheckString+"&f=portal&type=0&size=5"
	#print(sFlowURL)
	data = s.get(sFlowURL, headers=headers)
	print(data.json())'''
	#  获取工作流程里的已办结
def get_workflows(s):
	url = 'http://voa.grgbanking.com/HandlerGRGPortal.ashx'
	payload = {
	'method': 'getTDURL',
	'UserID': UserID
	}
	response = s.post(url, data=payload, headers=headers)
	url = response.json()['data']+'&url=%2Fgeneral%2Fworkflow%2Flist%2F'
	#print(url)
	s.get(url, headers=headers)
	cookie = s.cookies.get_dict()
	nd = str(int(time.time()))
	url = 'http://oa.grgbanking.com/general/workflow/list/getdata_over.php?TYPE=OVER&RUN_ID=&RUN_NAME=&FLOW_ID=null&TIME_OUT_FLAG=undefined&_search=false&nd=%s&rows=100&page=1&sidx=DELIVER_TIME&sord=desc'%nd
	workflow = s.get(url,cookies=cookie, headers=headers).json()
	workflows = workflow['rows']
	print(type(workflows))
	for wf in workflows:
		RUN_ID = wf['cell'][0]
		FLOW_ID = '2292'
		s = wf['cell'][2]
		res = re.match('.*?title=\"(.*?)\">',s)
		title = res.group(1)
		s = wf['cell'][4]
		res = re.match('.*?第(\d)步',s)
		PRCS_ID = res.group(1)
		print(title)
	
	# 查看流程详情
	'''RUN_ID = '' #流程号
	FLOW_ID = '' #流水号
	PRCS_ID = '' #步骤
	url = 'http://oa.grgbanking.com/general/workflow/list/print.php?RUN_ID=%s&FLOW_ID=%s&FLOW_VIEW=12345&PRCS_ID=%s&archive_time='%(RUN_ID, FLOW_ID, PRCS_ID)
	response = s.get(url,cookies=cookie, headers=headers)
	with open('work.html', 'w') as f:
		f.write(response.text.replace(u'\xa0', u''))'''
	'''filenanme = 1	
	while True:
		RUN_ID = input('输入工作流程号：')
		FLOW_ID = input('输入流水号：')
		PRCS_ID = input('输入步骤：')
		url = 'http://oa.grgbanking.com/general/workflow/list/print.php?RUN_ID=%s&FLOW_ID=%s&FLOW_VIEW=12345&PRCS_ID=%s&archive_time='%(RUN_ID, FLOW_ID, PRCS_ID)
		response = s.get(url,cookies=cookie, headers=headers)
		with open('%d.html'%filenanme, 'w') as f:
			f.write(response.text.replace(u'\xa0', u''))
		filenanme = filenanme+1'''
	
if __name__=='__main__':
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
	s = requests.session()
	login(s)
	#防止重认证
	try:
		get_workflows(s)
	except:
		login(s)
		get_workflows(s)
	
	