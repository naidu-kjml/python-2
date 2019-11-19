# -*-coding:utf-8 -*-
# author:xiaojiaming

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


class Email:
    def __init__(self, server, sender, password, receiver, title):

        self.title = title
        self.msg = MIMEMultipart('related')
        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def send(self,m):
        self.msg['Subject'] = Header(self.title,'utf-8')
        self.msg['From'] = Header(self.sender)
        self.msg['To'] = self.receiver
        content = MIMEText(m,'plain','utf-8')
        self.msg.attach(content)
        smtp_server = smtplib.SMTP(self.server)
        # smtp_server.set_debuglevel(1)
        smtp_server.starttls()
        smtp_server.login(self.sender,self.password)
        smtp_server.sendmail(self.sender,self.receiver,self.msg.as_string())
        smtp_server.close()
