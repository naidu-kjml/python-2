# coding=utf-8
import base64, requests
import rsa, urllib
from bs4 import BeautifulSoup


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

 
if __name__ == "__main__":
	s = requests.session()
	bash_url = 'http://voa.grgbanking.com/'
	response = s.get(bash_url)
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
	payload = {
	'method': 'GoToIndex',
	'USER_ID': 'lping12',
	'EMPID': 'G0108535',
	'USER_NAME': '罗苹'
	}
	url = 'http://voa.grgbanking.com/HandlerGoToIndex.ashx'
	response = s.post(url, data=payload)
	url = 'http://voa.grgbanking.com/Index.aspx'
	response = s.get(url)
	soup = BeautifulSoup(response.text, 'lxml')
	CheckString = soup.find('input', id='CheckString')['value']
	print(CheckString)
	sFlowURL = 'http://oa.grgbanking.com'+"/interface2/workflow_list2.php?"+CheckString+"&f=portal&type=0&size=5"
	print(sFlowURL)
	data = s.get(sFlowURL)
	print(data.json())
	