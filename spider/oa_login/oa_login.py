import requests,base64
from bs4 import BeautifulSoup


def str2key(s):
	# 对字符串解码
	b_str = base64.b64decode(s)
 
	if len(b_str) < 162:
		return False
 
	hex_str = ''
 
	# 按位转换成16进制
	for x in b_str:
		h = hex(ord(x))[2:]
		h = h.rjust(2, '0')
		hex_str += h
 
	# 找到模数和指数的开头结束位置
	m_start = 29 * 2
	e_start = 159 * 2
	m_len = 128 * 2
	e_len = 3 * 2
 
	modulus = hex_str[m_start:m_start + m_len]
	exponent = hex_str[e_start:e_start + e_len]
 
	return modulus,exponent
 
if __name__ == "__main__":
	bash_url = 'http://voa.grgbanking.com/'
	response = requests.get(bash_url)
	soup = BeautifulSoup(response.text,'lxml')
	pubkey = soup.find('input',id='tra')['value'] 
	key = str2key(pubkey)
	print(key)
