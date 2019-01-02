# coding: utf-8
from ftplib import FTP
import time
import tarfile
import os
# !/usr/bin/python
# -*- coding: utf-8 -*-


def ftpconnect(host,username,password):
	ftp = FTP()
	# ftp.set_debuglevel(2)
	ftp.connect(host,21)
	ftp.login(username, password)
	return ftp

#从ftp下载文件
def downloadfile(ftp, remotepath, localpath):
	bufsize = 1024
	fp = open(localpath, 'wb')
	ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)
	ftp.set_debuglevel(0)
	fp.close()

#从本地上传文件到ftp
def uploadfile(ftp, remotepath, localpath):
	bufsize = 1024
	fp = open(localpath, 'rb')
	ftp.storbinary('STOR ' + remotepath, fp, bufsize)
	ftp.set_debuglevel(0)
	fp.close()

if __name__ == "__main__":
	ftp = ftpconnect("ftp09.host.me0.cn","web2746","Jph8RCAK")
	downloadfile(ftp, "wwwroot/index.html", "index.html")
	#uploadfile(ftp, "C:/Users/Administrator/Desktop/test.mp4", "test.mp4")
	ftp.quit()