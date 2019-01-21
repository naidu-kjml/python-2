import requests
import re,os
import time
# 导入requests_toolbelt库使用MultipartEncoder
from requests_toolbelt import MultipartEncoder
local = time.strftime("%Y-%m-%d")
url = 'http://cn.bing.com/'
con = requests.get(url)
content = con.text
reg = r"(az/hprichbg/rb/.*?.jpg)"
a = re.findall(reg, content, re.S)[0]
print(a)
picUrl = url + a
read = requests.get(picUrl)
if not os.path.exists('pic'):
	os.mkdir('pic')
f = open('D:/bing/pic/%s.jpg' % local, 'wb')
f.write(read.content)
f.close()
time.sleep(3)
url = 'http://ftp09.host.me0.cn:3312/vhost/index.php?c=webftp&a=upsave'
headers = {
	'Cookie': 'Cookie: td_cookie=2936051868; PHPSESSID=tqb60frvuq0gmplmivbd3f6ob4',
	'Host': 'ftp09.host.me0.cn:3312',
	'Origin': 'http://ftp09.host.me0.cn:3312',
	'Referer': 'http://ftp09.host.me0.cn:3312/vhost/index.php?c=webftp&a=getfile&dir=16384&file=/wwwroot/images',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
	}
file_payload = {'file': ("background.jpg", open('D:/bing/pic/%s.jpg' % local, 'rb'), "image/jpeg")}
# 生成可用于multipart/form-data上传的数据
m = MultipartEncoder(file_payload)
# 自动生成Content-Type类型和随机码
headers['Content-Type'] = m.content_type
# 使用data上传文件
html = requests.post(url, headers=headers, data=m)