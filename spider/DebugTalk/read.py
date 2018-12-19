import csv,os,re
from mail import Email


with open('index.txt','r')as f:
	index = f.read()
with open('debugtalk.csv','r')as f:
	reader = csv.DictReader(f)
	rows = [row for row in reader]
title = rows[int(index)]['title']
link = rows[int(index)]['link']
time = rows[int(index)]['time']

e = Email('smtp.qq.com','981805032@qq.com','nmfavcrgtlfsbdeb','13250790293@163.com','DebugTalk文章：%s'%title)
e.send("文章：%s\n时间：%s\n链接：%s"%(title,time,link))
index = str(int(index)-1)
with open('index.txt','w')as f:
	f.write(index)