import time,sqlite3,subprocess,os,smtplib
from processBar import ShowProcess
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header

class sms(object):
	def __init__(self):
		self.sms_num = 0
#下载手机短信数据库
	def get_db(self):
		p = subprocess.Popen("adb shell su -c'cp data/data/com.android.providers.telephony/databases/mmssms.db /sdcard&&exit&&exit'",stdin=subprocess.PIPE,stdout=subprocess.PIPE)
		os.system("adb pull /sdcard/mmssms.db")

	
#从数据库获取短信
	def get_num(self):
		conn = sqlite3.connect('mmssms.db')
		cursor = conn.cursor()
		cursor.execute('select _id from sms order by _id desc LIMIT 1')
		self.sms_num = cursor.fetchall()[0][0]
		cursor.close()
		conn.close()

	def get_sms(self,num):
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
		
	def send_em(self,text):
		user = '981805032@qq.com'
		pwd = 'nmfavcrgtlfsbdeb'
		to = ['13250790293@163.com']
		msg = MIMEMultipart()
		msg['Subject'] = Header('短信', 'utf-8')
		msg['From'] = Header(user)

		content1 = MIMEText(text, 'plain', 'utf-8')
		msg.attach(content1)

		s = smtplib.SMTP('smtp.qq.com')
		s.set_debuglevel(1)              #调试使用
		s.starttls()                     #建议使用
		s.login(user, pwd)
		s.sendmail(user, to, msg.as_string())
		s.close()
		
		
		
if __name__=='__main__':
	print('程序启动中。。。。。。。。。。。。')
	s = sms()
	s.get_db()
	time.sleep(1)
	#初始短信数量
	s.get_num()
	sum = s.sms_num
	#循环次数
	t = 1
	time.sleep(1)
	print('当前短信数量为：%s'%sum)
	os.remove('mmssms.db')
	#开始循环
	while True:
		print(datetime.now())
		print('*********第%d次获取短信***********'%t)
		print('正在下载数据库')
		try:
			s.get_db()
			time.sleep(1)
			s.get_num()
		except:
			print('下载数据库失败，重新下载！！！！！！')
			continue
		print('下载完成')
		now = s.sms_num
		print('当前短信数量为：%s'%now)
		num = now-sum
		sum = s.sms_num
		print('收到新短信%d条'%num)
		if num>0:
			sms = s.get_sms(num)
			print('短信内容为：')
			print(sms)
			print('发送邮件中。。。。。。')
			for m in sms:
				s.send_em(m)
		os.remove('mmssms.db')
		print('距离下次获取短信还有10分钟')
#进度条
		max_steps = 100
		process_bar = ShowProcess(max_steps, 'OK')

		for i in range(max_steps):
			process_bar.show_process()
			time.sleep(6)
		t=t+1
	