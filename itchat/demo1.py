import itchat,time


@itchat.msg_register(itchat.content.TEXT)
def reply_msg(msg):
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	print(msg['Content'])
	itchat.send_msg('%s\n正在忙，稍后回复。。。'%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg['FromUserName'])

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
