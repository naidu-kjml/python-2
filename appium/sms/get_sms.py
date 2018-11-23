#-*-coding:utf-8 -*-'select _id from sms order by _id desc LIMIT 1'
import sqlite3
def sms(num):
	conn = sqlite3.connect('mmssms.db')
	cursor = conn.cursor()
	cursor.execute('select body from sms order by _id desc LIMIT ?', (num,))
	sms = cursor.fetchall()
	cursor.close()
	conn.close()
	con = []
	for s in range(len(sms)):
		con.append(sms[s][0])
	return con
	print(con)
