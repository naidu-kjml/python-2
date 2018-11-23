from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
import smtplib



user = '981805032@qq.com'
pwd = 'nmfavcrgtlfsbdeb'
to = ['13250790293@163.com']
msg = MIMEMultipart()
msg['Subject'] = Header('短信', 'utf-8')
msg['From'] = Header(user)
content1 = MIMEText('mess', 'plain', 'utf-8')
msg.attach(content1)
s = smtplib.SMTP('smtp.qq.com')
s.set_debuglevel(1)              #调试使用
s.starttls()                     #建议使用
s.login(user, pwd)
s.sendmail(user, to, msg.as_string())
s.close()