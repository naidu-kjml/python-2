#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests,os
from mail import *

loginurl='https://www.316e.net/data/renew.php?type=host&pid=2746'
raw_cookies='LoginEmail=981805032%40qq.com; LoginPass=fe3712cf16b044cf94a386935f25e740'
cookies={}
for line in raw_cookies.split(';'):  
	key,value=line.split('=',1)  
	cookies[key]=value
	
e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','xjming9@grgbanking.com','空间续期')
try:
	res=requests.get(loginurl,cookies=cookies)
except:
	e.send('续期失败')
if res.status_code!=200:
	print('续期失败：%s'%res.status_code)
	e.send('续期失败：%s'%res.status_code)
else:
	print('————————————————续期成功——————————————————————:%s'%res.status_code)

