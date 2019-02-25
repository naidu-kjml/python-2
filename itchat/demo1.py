import itchat,time


@itchat.msg_register(itchat.content.TEXT)
def reply_msg(msg):
    itchat.send_msg('洗澡中，程序自动回复。。。当前时间为：%s'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg['FromUserName'])


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
